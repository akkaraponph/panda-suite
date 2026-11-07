`label(request)` returns a string containing the request’s `id`, a colon and space, and its `status`.

For example, `label({"id": 42, "status": "pending"})` returns `"42: pending"`.

It reads those two dictionary keys without modifying the request. If either key is missing, it raises `KeyError`.
