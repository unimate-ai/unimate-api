class UserDoesNotExistsException(Exception):
    def __init__(self, message: str = "User does not exist!"):
        super(UserDoesNotExistsException, self).__init__(message)

