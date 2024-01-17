from pydantic import BaseModel


class GenreType(BaseModel):
    genre_type_id: int
    genre_type_description: str