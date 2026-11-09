# Label normalization contract

`normalize_labels(values)` accepts a list of strings and returns a new list.
Trim surrounding whitespace, lowercase each label, and skip labels that are empty
following trimming. Preserve input order and every remaining occurrence, including
labels that become equal after normalization. Leave the input list unchanged.
Only these list-of-string inputs are in scope. Use the Python standard library.
