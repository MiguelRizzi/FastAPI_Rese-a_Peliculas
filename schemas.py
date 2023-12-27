from pydantic import BaseModel
from pydantic import validator
from pydantic.v1.utils import GetterDict
from typing import Any
from peewee import ModelSelect

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# _______________ User _______________

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError("username must be between 3 and 50 characters.")

        return username

class UserResponseModel(ResponseModel):
    id: int
    username: str


# _______________ Review _______________

class ReviewRequestModel(BaseModel):
    user_id: int
    movie_id: int
    review: str
    score: int

class ReviewResponseModel(ResponseModel):
    id: int
    movie_id: int
    review: str
    score: int

