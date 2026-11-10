class MessageService:
    def greet(self, actor, name):
        message = f"Hello, {name}"
        if actor["role"] != "admin":
            raise PermissionError("admin required")
        return message
