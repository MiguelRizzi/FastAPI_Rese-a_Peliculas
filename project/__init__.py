from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from fastapi.security import OAuth2PasswordRequestForm

from .database import database as connection
from .database import User
from .database import Movie
from .database import UserReview

from .routers import user_router
from .routers import movie_router
from .routers import review_router

from .common import create_access_token

app = FastAPI(
    title="Movie Reviews",
    description="Project to create movie reviews",
    version="1.0",
)
api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(movie_router)
api_v1.include_router(review_router)


@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)

    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'bearer'
        }
    else:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )


app.include_router(api_v1)


#eventos
@app.on_event("startup")
def startupp():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User, Movie, UserReview])
    
@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()

