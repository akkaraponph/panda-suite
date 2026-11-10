"""Mutation tests for package integrity and installation safety."""

import json
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
validate = runpy.run_path(str(ROOT / "scripts/validate-skills.py"))["validate"]
verify_vendor = runpy.run_path(str(ROOT / "scripts/vendor-upstreams.py"))["verify"]
install = runpy.run_path(str(ROOT / "scripts/install-skills.py"))["install"]
restore = runpy.run_path(str(ROOT / "scripts/vendor-upstreams.py"))["restore"]
prepare = runpy.run_path(str(ROOT / "scripts/prepare-evaluation.py"))["prepare"]


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "suite"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "runs", "dist"
        ))

    def test_package_is_valid(self):
        self.assertEqual([], validate(self.root))
        self.assertEqual([], verify_vendor(self.root))

    def test_integrated_sources_are_primary_skills(self):
        self.assertFalse((self.root / "third_party").exists())
        lock = json.loads((self.root / "upstream-lock.json").read_text())
        destinations = {
            item["destination"]
            for source in lock["upstreams"]
            for item in source["files"]
        }
        self.assertIn("vendor/panda-debugger/SKILL.md", destinations)
        for destination in destinations:
            self.assertTrue(
                destination.startswith("skills/")
                or destination == "vendor/panda-debugger/SKILL.md"
            )
        self.assertTrue((self.root / "skills/panda-debugger/SKILL.md").is_file())
        for name in ["panda-debugger", "buddhist-method"]:
            self.assertTrue(any((self.root / "skills" / name / "references").glob("*.md")))

    def test_yaml_is_really_parsed(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text("---\nname: [invalid\ndescription: broken\n---\nBody")
        self.assertTrue(any("YAML" in e for e in validate(self.root)))

    def test_duplicate_yaml_keys_rejected(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text("---\nname: panda-plan\nname: other\ndescription: Plan work\n---\nBody")
        self.assertTrue(any("duplicate" in e.lower() for e in validate(self.root)))

    def test_name_must_match_folder(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text(p.read_text().replace("name: panda-plan", "name: bad--name"))
        self.assertTrue(any("name" in e for e in validate(self.root)))

    def test_broken_reference_detected(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text(p.read_text() + "\nSee [required guide](references/missing.md).\n")
        self.assertTrue(any("missing.md" in e for e in validate(self.root)))

    def test_reference_definition_cannot_escape_skill(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text(p.read_text() + "\nRead [required][guide].\n\n[guide]: ../../README.md\n")
        self.assertTrue(any("standalone" in e for e in validate(self.root)))

    def test_missing_reference_definition_detected(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text(p.read_text() + "\nRead [required][guide].\n")
        self.assertTrue(any("undefined" in e for e in validate(self.root)))

    def test_titled_reference_and_encoded_path_are_valid(self):
        folder = self.root / "skills/panda-plan"
        (folder / "references").mkdir(exist_ok=True)
        (folder / "references/a guide.md").write_text("Guide")
        p = folder / "SKILL.md"
        p.write_text(p.read_text() + '\nRead [guide](references/a%20guide.md "Title").\n')
        self.assertEqual([], validate(self.root))

    def test_skill_cannot_require_outside_reference(self):
        p = self.root / "skills/panda-plan/SKILL.md"
        p.write_text(p.read_text() + "\nRead [shared](../../README.md).\n")
        self.assertTrue(any("standalone" in e for e in validate(self.root)))

    def test_missing_skill_detected(self):
        shutil.rmtree(self.root / "skills/panda-manual")
        self.assertTrue(any("panda-manual" in e for e in validate(self.root)))

    def test_manifest_identity_drift_detected(self):
        p = self.root / ".claude-plugin/plugin.json"
        data = json.loads(p.read_text())
        data["name"] = "wrong-plugin"
        p.write_text(json.dumps(data))
        self.assertTrue(any("identity" in e for e in validate(self.root)))

    def test_manifest_path_escape_detected(self):
        p = self.root / ".claude-plugin/plugin.json"
        data = json.loads(p.read_text())
        data["skills"] = "./../outside/"
        p.write_text(json.dumps(data))
        self.assertTrue(any("path" in e.lower() for e in validate(self.root)))

    def test_suite_rejects_noncanonical_skill_paths(self):
        p = self.root / ".claude-plugin/plugin.json"
        data = json.loads(p.read_text())
        for value in ["./docs/", []]:
            with self.subTest(value=value):
                data["skills"] = value
                p.write_text(json.dumps(data))
                self.assertTrue(any("canonical" in e for e in validate(self.root)))

    def test_vendor_drift_detected(self):
        p = self.root / "vendor/panda-debugger/SKILL.md"
        p.write_text(p.read_text() + "\nchanged\n")
        self.assertTrue(any("sha256" in e for e in verify_vendor(self.root)))

    def test_vendor_destination_escape_detected(self):
        p = self.root / "upstream-lock.json"
        data = json.loads(p.read_text())
        data["upstreams"][0]["files"][0]["destination"] = "../outside"
        p.write_text(json.dumps(data))
        self.assertTrue(any("path" in e.lower() for e in verify_vendor(self.root)))

    def test_install_one_skill_is_self_contained(self):
        dest = Path(self.temp.name) / "agent-skills"
        install(self.root, dest, ["panda-spec"])
        self.assertTrue((dest / "panda-spec/SKILL.md").is_file())
        self.assertTrue((dest / "panda-spec/references/specification.md").is_file())
        self.assertEqual(["panda-spec"], sorted(p.name for p in dest.iterdir()))

    def test_collision_does_not_partially_install(self):
        dest = Path(self.temp.name) / "agent-skills"
        (dest / "panda-plan").mkdir(parents=True)
        (dest / "panda-plan/mine.txt").write_text("keep")
        with self.assertRaises(FileExistsError):
            install(self.root, dest, ["panda-lead", "panda-plan"])
        self.assertFalse((dest / "panda-lead").exists())
        self.assertEqual("keep", (dest / "panda-plan/mine.txt").read_text())

    def test_late_collision_cannot_report_success(self):
        dest = Path(self.temp.name) / "agent-skills"
        original = Path.mkdir

        def racing_mkdir(path, *args, **kwargs):
            if path == dest / "panda-plan":
                original(path)
                (path / "SKILL.md").write_text("Existing user skill")
            return original(path, *args, **kwargs)

        with patch.object(Path, "mkdir", racing_mkdir), self.assertRaises(FileExistsError):
            install(self.root, dest, ["panda-lead", "panda-plan"])
        self.assertFalse((dest / "panda-lead").exists())
        self.assertEqual("Existing user skill", (dest / "panda-plan/SKILL.md").read_text())

    def test_install_rejects_unknown_skill_and_traversal(self):
        for name in ["missing", "../README.md"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                install(self.root, Path(self.temp.name) / "dest", [name])

    def test_install_rejects_symlink(self):
        source = self.root / "skills/panda-plan"
        (source / "leak").symlink_to(self.root / "README.md")
        with self.assertRaises(ValueError):
            install(self.root, Path(self.temp.name) / "dest", ["panda-plan"])

    def test_restore_clean_checkout_needs_no_fetch(self):
        self.assertEqual(0, restore(self.root))

    def test_restore_refuses_modified_upstream(self):
        p = self.root / "vendor/panda-debugger/SKILL.md"
        p.write_text(p.read_text() + "\nlocal change\n")
        with self.assertRaisesRegex(ValueError, "overwrite local change"):
            restore(self.root)

    def test_adapted_skill_is_not_a_pinned_restore_target(self):
        p = self.root / "skills/panda-debugger/SKILL.md"
        p.write_text(p.read_text() + "\nlocal adaptation\n")
        self.assertEqual(0, restore(self.root))
        self.assertTrue(p.read_text().endswith("local adaptation\n"))

    def test_every_skill_installs_independently(self):
        local_links = runpy.run_path(str(ROOT / "scripts/validate-skills.py"))["local_links"]
        for source in sorted((self.root / "skills").iterdir()):
            with self.subTest(skill=source.name):
                dest = Path(self.temp.name) / ("single-" + source.name)
                install(self.root, dest, [source.name])
                self.assertEqual([source.name], [p.name for p in dest.iterdir()])
                for document in (dest / source.name).rglob("*.md"):
                    self.assertEqual([], local_links(document, dest / source.name, standalone=True))

    def test_scenario_integrity_checks(self):
        p = self.root / "tests/scenarios/cases.json"
        original = json.loads(p.read_text())
        for field, value, expected in [
            ("fixture", "../../outside", "fixture"),
            ("fixture", "absent", "fixture"),
            ("prompt", "", "prompt"),
            ("checks", [], "checks"),
        ]:
            with self.subTest(field=field, value=value):
                cases = json.loads(json.dumps(original))
                cases[0][field] = value
                p.write_text(json.dumps(cases))
                self.assertTrue(any(expected in e for e in validate(self.root)))

    def test_refactor_preparation_keeps_oracles_out(self):
        cases = json.loads((self.root / "tests/scenarios/cases.json").read_text())
        for case in cases:
            if not case["id"].startswith("REFACTOR-"):
                continue
            with self.subTest(case=case["id"]):
                dest = Path(self.temp.name) / case["id"]
                prepare(self.root, dest, case["id"], "specialist")
                self.assertFalse((dest / "cases.json").exists())
                self.assertFalse((dest / "check_refactor.py").exists())
                self.assertFalse((dest / "reviewer").exists())
                task = (dest / "TASK.txt").read_text()
                for check in case["checks"]:
                    self.assertNotIn(check, task)

    def test_fixture_preparation_excludes_answer_key(self):
        dest = Path(self.temp.name) / "blind-case"
        prepare(self.root, dest, "B", "baseline")
        self.assertTrue((dest / "service.py").is_file())
        prompt = (dest / "TASK.txt").read_text()
        self.assertNotIn("checks", prompt)
        self.assertNotIn("Routes only", prompt)
        self.assertFalse((dest / "cases.json").exists())
        with self.assertRaises(FileExistsError):
            prepare(self.root, dest, "B", "lead")

    def test_learn_preparation_keeps_reviewer_control_out(self):
        cases = json.loads((self.root / "tests/scenarios/cases.json").read_text())
        for case in cases:
            if not case["id"].startswith("LEARN-"):
                continue
            for arm in ("baseline", "specialist", "lead"):
                with self.subTest(case=case["id"], arm=arm):
                    dest = Path(self.temp.name) / (case["id"] + arm)
                    prepare(self.root, dest, case["id"], arm)
                    self.assertFalse((dest / "reviewer").exists())
                    self.assertFalse((dest / "learn-control").exists())
                    self.assertFalse((dest / "check_learn.py").exists())
                    self.assertFalse((dest / "cases.json").exists())
                    self.assertEqual((self.root / "tests/fixtures/learn-orders/storage.py").read_bytes(),
                                     (dest / "storage.py").read_bytes())
                    task = (dest / "TASK.txt").read_text()
                    for check in case["checks"]:
                        self.assertNotIn(check, task)


if __name__ == "__main__":
    unittest.main()
