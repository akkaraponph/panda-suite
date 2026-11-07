`label(request)` returns a string containing the request's `id`, a colon and space, and its `status` (`service.py:12–13`). For example, `label({"id": 1, "status": "pending"})` returns `"1: pending"`.

It reads those two keys without changing the request or performing approval. A missing `id` or `status` key raises `KeyError` for an ordinary dictionary.
