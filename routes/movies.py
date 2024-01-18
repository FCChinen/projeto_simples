from sqlalchemy.orm import Session
from models.movies import MovieDescription, Movies
import sql_app.models as models


def add_movie(movies: Movies, db: Session):
    db_movie = models.Movies(movies)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie