from pydantic import BaseModel


class GenreType(BaseModel):
    genre_id: int
    genre_name: str

    class Config:
        orm_mode = True
