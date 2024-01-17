from sqlalchemy.orm import Session
import sql_app.models as models


def insert_genre_type(db: Session, genre_name: str):
    db_genre = models.GenreType(genre_name=genre_name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genre_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GenreType).offset(skip).limit(limit).all()