from pydantic import BaseModel
from pydantic import validator

class UserBaseModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError("username must be between 3 and 50 characters.")

        return username