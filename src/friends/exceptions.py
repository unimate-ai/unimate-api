class FriendAlreadyExistsException(Exception):
    def __init__(self, message="Friend connection already exist"):
        super().__init__(message)
        self.message = message