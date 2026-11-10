class Formatter:
    def build(self, name):
        return f"Hello, {name}"


class MessageService:
    def __init__(self):
        self.formatter = Formatter()

    def greet(self, actor, name):
        if actor["role"] != "admin":
            raise PermissionError("admin required")
        return self.formatter.build(name)
