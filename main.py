from fastapi import FastAPI
from fastapi import HTTPException
from database import database as connection
from database import User
from database import Movie
from database import UserReview
from schemas import UserRequestModel
from schemas import UserResponseModel
from schemas import ReviewRequestModel
from schemas import ReviewResponseModel
from schemas import ReviewRequestPutModel
from typing import List

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

@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review



@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews():
    reviews = UserReview.select()


    return [user_review for user_review in reviews]

@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review (review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return user_review

@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()

    return user_review

@app.delete('/reviews/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.delete_instance()

    return user_review