from pydantic import EmailStr
from fastapi import HTTPException
from http import HTTPStatus

class InterestAlreadyExistsException(Exception):
    def __init__(self, message: str = "Interest already exists!"):
        super(InterestAlreadyExistsException, self).__init__(message)

