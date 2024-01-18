from pydantic import BaseModel, Field
from typing import Optional
from . import genre_type_response
from datetime import date
from decimal import Decimal


class MovieDescription(BaseModel):
    score: Decimal
    cast: str
    director: str
    synopsis: str


class Movies(BaseModel):
    name: str
    launch_date: date

    fk_genre_id: int


class MovieDescriptionResponse(MovieDescription):
    movie_description_id: int


class MoviesResponse(Movies):
    movie_id: int


class FullMovie(MoviesResponse, MovieDescription):
    class Config:
        orm_mode = True


class ModifyMovies(BaseModel):
    movie_id: int
    name: Optional[str] = Field(None)
    launch_date: Optional[date] = Field(None)
    fk_genre_id: Optional[int] = Field(None)


class ModifyMovieDescription(BaseModel):
    movie_id: int

    score: Optional[Decimal] = Field(None)
    cast: Optional[str] = Field(None)
    director: Optional[str] = Field(None)
    synopsis: Optional[str] = Field(None)


class ModifyMovieDescriptionResponse(MovieDescription):
    fk_movie_id: int