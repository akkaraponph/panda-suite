#!/usr/bin/env python3
"""Check the blind Logo fixtures and a locally rendered package control."""

import base64
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import struct
import subprocess
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
NS = "{http://www.w3.org/2000/svg}"


def svg(path):
    return ET.parse(path).getroot()


def png_dimensions(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    stream = io.BytesIO(data[8:])
    width = height = None
    while length_bytes := stream.read(4):
        length, = struct.unpack(">I", length_bytes)
        kind, body = stream.read(4), stream.read(length)
        crc, = struct.unpack(">I", stream.read(4))
        assert zlib.crc32(kind + body) == crc
        if kind == b"IHDR":
            width, height, _, color_type, _, _, _ = struct.unpack(">IIBBBBB", body)
            assert color_type in (4, 6), "expected an alpha channel"
        if kind == b"IEND":
            assert width and height and not stream.read()
            return width, height
    raise AssertionError("PNG missing IEND")


def verify_package(path):
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == len(set(names))
        for name in names:
            relative = PurePosixPath(name)
            assert not relative.is_absolute() and ".." not in relative.parts
            assert not ("\\" in name or ":" in name)
        assert all(not stat.S_ISLNK(info.external_attr >> 16) for info in archive.infolist())
        manifest = json.loads(archive.read("manifest.json"))
        assert manifest["project"] and manifest["palette"] and manifest["provenance"]
        assert manifest["verification"]
        assets = manifest["assets"]
        assert len(assets) + 1 == len(names)
        assert set(names) == {"manifest.json", *(asset["path"] for asset in assets)}
        for asset in assets:
            assert asset["name"]
            data = archive.read(asset["path"])
            if asset["format"] == "png":
                assert list(png_dimensions(data)) == asset["dimensions"]
            elif asset["format"] == "svg":
                assert ET.fromstring(data).tag == NS + "svg"
            else:
                raise AssertionError(asset["format"])


def main():
    control = FIXTURES / "logo-raster/control.svg"
    candidate = svg(FIXTURES / "logo-raster/candidate.svg")
    image = candidate.find(NS + "image")
    assert image is not None and len(candidate) == 1
    assert png_dimensions(base64.b64decode(image.attrib["href"].split(",", 1)[1])) == (1, 1)
    master = svg(control)
    assert master.tag == NS + "svg" and master.get("viewBox") == "0 0 64 64"
    assert master.find(NS + "path") is not None and master.find(NS + "image") is None
    reference = FIXTURES / "logo-reference"
    assert svg(reference / "current.svg").find(NS + "text").text == "Tide Legder"
    assert svg(reference / "reference.svg").find(NS + "image").get("href").startswith("https://")
    print("Passed SVG vector/raster control, wordmark, and untrusted-reference fixtures")

    renderer = shutil.which("rsvg-convert")
    if renderer is None:
        print("Not Run rendered PNG and ZIP control (rsvg-convert unavailable)")
        return
    with TemporaryDirectory() as work:
        directory = Path(work)
        assets = [{"name": "Master icon", "path": "icon.svg", "format": "svg"}]
        for size in (16, 24, 32, 512):
            name = f"icon-{size}.png"
            subprocess.run([renderer, "-w", str(size), "-h", str(size),
                            "-o", str(directory / name), str(control)], check=True)
            assets.append({"name": f"{size} px icon", "path": name, "format": "png",
                           "dimensions": [size, size]})
        package = directory / "kit.zip"
        manifest = {
            "project": "Tide Ledger",
            "palette": ["#173447"],
            "provenance": "Synthetic reviewer control",
            "verification": "PNG metadata and ZIP integrity checked by this script",
            "assets": assets,
        }
        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("manifest.json", json.dumps(manifest))
            archive.write(control, "icon.svg")
            for asset in assets[1:]:
                name = asset["path"]
                archive.write(directory / name, name)
        verify_package(package)
        with zipfile.ZipFile(package, "a") as archive:
            archive.writestr("unlisted.txt", "Unexpected member")
        try:
            verify_package(package)
        except AssertionError:
            print("Passed rendered PNG metadata and ZIP/manifest control; rejected extra ZIP member")
        else:
            raise AssertionError("Package check accepted a member omitted from the manifest")


if __name__ == "__main__":
    main()
