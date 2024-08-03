class ChatroomAlreadyExistsException(Exception):
    def __init__(self, message="Chatroom with these participants already exist"):
        super().__init__(message)
        self.message = message
