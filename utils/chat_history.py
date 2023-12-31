class ChatHistory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ChatHistory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.messages = []
            self.buffer = ""
            self.current_role = None
            self.initialized = True

    def set_role(self, role):
        self.current_role = role

    def save(self, message, end="\n"):
        if self.current_role is None:
            raise ValueError("Role is not set")
        self.buffer += message + end

    def log(self, message, end="\n"):
        self.save(message, end=end)
        print(message, end=end)

    def flush(self):
        if self.buffer:
            self.messages.append({"role": self.current_role, "content": self.buffer})
            self.buffer = ""

    def get_messages(self):
        return self.messages

    def clear_history(self):
        self.messages = []
        self.buffer = ""
