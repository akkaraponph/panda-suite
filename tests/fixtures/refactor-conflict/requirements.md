# Labels contract
normalize_labels accepts lists of strings. Trim whitespace, lowercase, skip empty
labels, preserve order and every nonempty occurrence including duplicates.
Return a new list and leave inputs unchanged. Structural work must preserve
observable behavior; disclose any existing source/requirement discrepancy before
choosing a correction. Use the Python standard library.
Run `python3 -B -m unittest -v` from this directory.
