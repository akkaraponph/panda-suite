The greeting itself is simple; the design adds four classes and three collaborating objects for one role check and one formatted string. `MessageAdapter.build()` only forwards to `MessageFactory.build()`; neither adds behavior needed by this use case.

The smallest sensible change preserves the existing `MessageService().greet(actor, name)` calling shape and puts both operations directly in that method:

```python
class MessageService:
    def greet(self, actor, name):
        if actor["role"] != "admin":
            raise PermissionError("admin required")
        return f"Hello, {name}"
```

Remove `Validator`, `MessageFactory`, `MessageAdapter`, and the constructor if they have no external callers. The supplied file contains no other use of those helpers; check repository call sites before removing externally imported names. A standalone `greet` function could be smaller still, but would change the current calling interface without a demonstrated need.

Preserve the exact role comparison, exception and message, authorization-before-formatting order, and greeting text. Keep the existing `KeyError` for a missing `role`; adding a default would change behavior. No dependency injection, configurable validation, interfaces, or factories are needed for the stated use case.

Read-only execution verified `admin` returns `Hello, Ada`, `member` raises `PermissionError("admin required")`, and an actor without `role` raises `KeyError("role")`. For an eventual refactor, also check empty names and that a denied request does not format the name. No source files were edited and no automated test suite was supplied or claimed.
