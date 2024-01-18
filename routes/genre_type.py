from sqlalchemy.orm import Session
from fastapi import HTTPException
import sql_app.models as models


def insert_genre_type(db: Session, genre_name: str):
    db_genre = models.GenreType(genre_name=genre_name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genre_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GenreType).offset(skip).limit(limit).all()


def delete_genre_types(genre_id: int, genre_name: str, db: Session):
    if genre_id:
        db_object = db.query(models.GenreType)\
            .filter(models.GenreType.genre_id == genre_id)\
            .first()
        if db_object is None:
            raise HTTPException(
                status_code=404,
                detail="Current genre_id was not found in db."
            )
        db.delete(db_object)
        db.commit()
        return [db_object.__dict__]
    else:
        db_objects = db.query(models.GenreType)\
            .filter(models.GenreType.genre_name == genre_name)\
            .all()
        if db_objects == []:
            raise HTTPException(
                status_code=404,
                detail="Current genre_name was not found in db."
            )
        db_object_list = []
        print(f"genre_name resposta do db: {db_objects}")
        for db_object in db_objects:
            db.delete(db_object)
            db_object_list.append(db_object.__dict__)
        db.commit()
        return db_object_list


def update_genre_types(genre_id: int, genre_name: str, db: Session):
    db_object = db.query(models.GenreType)\
        .filter(models.GenreType.genre_id == genre_id)\
        .first()
    if db_object is None:
        raise HTTPException(
            status_code=404,
            detail="Current genre_id was not found in db."
        )
    db_object.genre_name = genre_name
    db.commit()
    db_object = db.query(models.GenreType)\
        .filter(models.GenreType.genre_id == genre_id)\
        .first()
    return db_object.__dict__
