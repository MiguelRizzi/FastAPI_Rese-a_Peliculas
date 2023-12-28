from fastapi import APIRouter
from fastapi import HTTPException

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel

router = APIRouter(prefix='/users')

@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail="User already exists.")

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_password
    )
    return user
