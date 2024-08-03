from pydantic import EmailStr
from fastapi import HTTPException
from http import HTTPStatus

class UserAlreadyExistsException(Exception):
    def __init__(self, user_email: EmailStr = "", message: str = "User already exists!"):
        if user_email:
            message = f"User ({user_email}) already exists!"

        super(UserAlreadyExistsException, self).__init__(message)
        self.user_email = user_email

class RegistrationFailedException(Exception):
    def __init__(self, message="Error while registering new user"):
        super().__init__(message)
        self.message = message

class UnauthorizedOperationException(Exception):
    def __init__(self, message="Unauthorized operation. You may have to log in with the necessary permissions to perform this action."):
        super().__init__(message)
        self.message = message

class UserDoesNotExistsException(Exception):
    def __init__(self, message: str = "User does not exist!"):
        super(UserDoesNotExistsException, self).__init__(message)