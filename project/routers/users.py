from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from fastapi import Response
from fastapi import Cookie

from typing import List

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel

from ..schemas import ReviewResponseModel

router = APIRouter(prefix='/users')

@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(status_code=409, detail="User already exists.")

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_password
    )
    return user

@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.password !=User.create_password(credentials.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    response.set_cookie(key="user_id", value=user.id)
    return user
  
@router.get('/reviews', response_model= List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return [user_review for user_review in user.reviews]