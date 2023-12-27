from fastapi import FastAPI
from fastapi import HTTPException
from database import database as connection
from database import User
from database import Movie
from database import UserReview
from schemas import UserRequestModel
from schemas import UserResponseModel

app = FastAPI(
    title="Movie Reviews",
    description="Project to create movie reviews",
    version="1.0",
)

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

@app.get("/")
async def index():
    return "Welcome - Movie Reviews API"

@app.get("/about")
async def about():
    return "About"


@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail="User already exists.")

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_password
    )
    return user