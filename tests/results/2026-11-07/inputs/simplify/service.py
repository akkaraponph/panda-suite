class Validator:
    def check(self, actor):
        if actor["role"] != "admin":
            raise PermissionError("admin required")


class MessageFactory:
    def build(self, name):
        return f"Hello, {name}"


class MessageAdapter:
    def __init__(self, factory):
        self.factory = factory

    def build(self, name):
        return self.factory.build(name)


class MessageService:
    def __init__(self):
        self.validator = Validator()
        self.adapter = MessageAdapter(MessageFactory())

    def greet(self, actor, name):
        self.validator.check(actor)
        return self.adapter.build(name)
