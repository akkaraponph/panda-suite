Keep `MessageService().greet(actor, name)` and move its two operations directly into `greet`:

```python
class MessageService:
    def greet(self, actor, name):
        if actor["role"] != "admin":
            raise PermissionError("admin required")
        return f"Hello, {name}"
```

`service.py:12–17` is a pass-through adapter; `service.py:7–9` only formats one string. The constructor at lines 21–23 builds three collaborators for a single fixed use case, adding names, indirection, and object wiring without demonstrated variation. The permission rule in lines 3–4 is essential; retaining it inside the existing public method removes the unnecessary structure without dropping authorization. Keep the class and method call shape to avoid forcing caller changes.

Preserve the exact admin role comparison, `PermissionError("admin required")`, missing-role `KeyError`, guard-before-format order, and f-string output (including empty and Unicode names). Do not add name validation, role defaults, plugins, dependency injection, or speculative configuration. The direct method can accommodate another concrete greeting behavior later without an interface framework now.

Trade-off: factory/adapter/validator classes and mutable `service.validator`/`service.adapter` attributes would disappear. No callers or tests are supplied to establish them as supported extension points. Before applying this proposal in a wider repository, search for imports, direct attribute access, and monkeypatching; retain a compatibility shim only for a demonstrated consumer. Reverting the small refactor would restore the original structure if such a consumer is found.

Verification: executed the current implementation for admin/member/missing role and empty name. Also executed the proposed class in memory and compared return values or exception types/arguments across 12 combinations of those actors and normal, empty, Unicode, and None names; all matched. These representative checks support the recommendation, not full repository compatibility. No source files edited and no supplied test suite exists in this fixture.
