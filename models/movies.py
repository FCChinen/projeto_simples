from pydantic import BaseModel
from . import genre_type_response
from datetime import date
from decimal import Decimal


class MovieDescription(BaseModel):
    movie_description_id: int
    fk_movie_id: int
    score: Decimal
    cast: str
    director: str
    synopsis: str


class Movies(BaseModel):
    name: str
    launch_date: date

    fk_genre_id1: int
    fk_genre_id2: int
    fk_genre_id3: int