# Greeting contract
Preserve the public MessageService constructor and greet(actor, name), and
consumer.welcome. Admin gets exactly "Hello, <name>". Other roles raise
PermissionError("admin required"). Missing role raises KeyError. Authorization
must run before formatting name; denial must not call its __str__.
The formatter is an internal implementation detail. Use standard-library Python.
Run `python3 -B -m unittest -v` from this directory.
