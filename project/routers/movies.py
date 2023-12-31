from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from typing import List

from ..schemas import MovieRequestModel
from ..schemas import MovieResponseModel

from ..database import Movie
from ..database import User

from ..common import get_current_user


router = APIRouter(prefix='/movies')

@router.get('', response_model=List[MovieResponseModel])
async def get_movies(page:int = 1, limit:int = 10):

    movies = Movie.select().paginate(page, limit)

    return [movie for movie in movies]

@router.get('/{movie_id}', response_model=MovieResponseModel)
async def get_movie(movie_id: int):

    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie

@router.post('', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel, user: User = Depends(get_current_user)):

    movie = Movie.create(
        title = movie.title,
        user_id = user.id
    )

    return movie

@router.put('/{movie_id}', response_model=MovieResponseModel)
async def update_movie(movie_id: int, movie_request: MovieRequestModel, user: User = Depends(get_current_user)):

    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this movie")


    movie.title = movie_request.title
    movie.save()

    return movie

@router.delete('/{movie_id}', response_model=MovieResponseModel)
async def delete_movie(movie_id: int, user: User = Depends(get_current_user)):

    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this movie")

    movie.delete_instance()
  
    return movie
