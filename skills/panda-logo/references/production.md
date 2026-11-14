# SVG, rendering, and asset packaging

## Build a portable master

Use well-formed XML with the SVG namespace, a positive explicit viewBox, stable
aspect ratio, and editable paths, geometric primitives, or grouped geometry.
Group icon and wordmark separately when useful, and use meaningful IDs. Keep
geometry and paint simple enough to inspect and maintain. Avoid unnecessary
filters and gradients. Keep editable and optimized sources separate if
optimization removes editing information.

A raster logo wrapped in SVG is still raster. Build actual vectors for master
deliverables. Use path outlines for portable typography where permitted. Preserve
the exact wording and check spacing, kerning, and proportion. If text remains
live, record its font and fallback behavior. Record artwork and font provenance,
licenses where known, and whether image generation or manual reconstruction was
used. Confirm rights before redistributing fonts or third-party source artwork.

Inspect untrusted SVG as data before rendering. Use a parser with external entity
resolution and network access disabled, and reject DTDs, scripts, event handlers,
foreign content, and remote/file references, including URLs in CSS and fonts.
Use a sanitized working copy or rebuild safe geometry if necessary. Never open
unvetted SVG in an active browser or modify an original during an audit. Export
self-contained geometry without hidden raster dependencies or active content.

## Export requested variants

Choose an installed or host-provided SVG renderer or converter and verify a
sample before batching. Inspect the generated pixels as well as file metadata.
When conversion or visual inspection is unavailable, report the affected
exports/checks and use the remaining tools. A valid SVG source can still be
delivered without a preview. Verify any ZIP against the actual authorized files.

Keep geometry consistent across derivatives. Recompose horizontal, stacked, or
icon-only lockups using the same mark. Check centered icons, safe margins,
clipping, aspect ratio, and real alpha where requested. Inspect the actual mark
at 24 and 32 px, and at 16 px for favicons. Compare monochrome and light/dark
versions for loss of detail, edge definition, and contrast. Supported platform
specifications and user settings take priority over these working presets.

| Asset | Preset |
| --- | --- |
| README banner | 1600 × 480 |
| GitHub social preview | 1280 × 640 |
| Avatar | 512 × 512 |
| App icon | 1024 × 1024 |
| Favicon | 16, 32, 48 px |
| General icon | 128, 256, 512 px |

Verify current platform specifications against authoritative documentation when
platform compliance is requested. Include a contact sheet, palette, or usage
notes when the kit calls for them.

## Verify the package

Use the requested destination. A practical kit layout is
`brand/<project>/` with `source/`, `logos/`, `icons/`, `banners/`,
`social/`, and `preview/` as needed. Include `brand-guidelines.md` when
usage guidance is requested. For a ZIP, include `manifest.json` with the
project name, palette, source and provenance, verification and limitations, and
an `assets` array with one record per deliverable. Include name, relative path,
format, and pixel dimensions where applicable. Keep the manifest as a package index, separate from its asset
records.

Reopen each requested asset. Match file format, dimensions, and transparency
to the brief and the manifest. Make the ZIP from an explicit list of deliverables
and the manifest. Reopen it, test member integrity, and compare its file list
with the manifest and any documented package files. Reject duplicate, absolute,
parent-traversal, and symlink entries. Keep temporary files, caches, and unrelated
project content out of the ZIP.
