from sqlalchemy.orm import Session
from models.movies import MovieDescription, Movies, ModifyMovieDescription, ModifyMovies
from fastapi import HTTPException
import sql_app.models as models


def add_movie(movies: Movies, movie_description: MovieDescription, db: Session):
    genre_obj = db.query(models.GenreType)\
        .filter(models.GenreType.genre_id == movies.fk_genre_id)\
        .first()
    if not genre_obj:
        raise HTTPException(
            status_code=422,
            detail="Invalid genre_type"
        )
    movie_obj = db.query(models.Movies)\
        .filter(models.Movies.name == movies.name)\
        .first()
    if movie_obj:
        raise HTTPException(
            status_code=422,
            detail="Movie already exists"
        )
    db_movie = models.Movies(
        name=movies.name,
        launch_date=movies.launch_date,
        fk_genre_id=movies.fk_genre_id
        )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    movie = db_movie.__dict__.copy()
    db_movie_description = models.MovieDescriptions(
        fk_movie_id=db_movie.movie_id,
        score=movie_description.score,
        cast=movie_description.cast,
        director=movie_description.director,
        synopsis=movie_description.synopsis
        )
    db.add(db_movie_description)
    db.commit()
    db.refresh(db_movie_description)
    return movie | db_movie_description.__dict__


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movies).offset(skip).limit(limit).all()


def delete_movie(movie_id: int, db: Session):
    db_object = db.query(models.Movies, models.MovieDescriptions)\
        .outerjoin(
            models.MovieDescriptions,
            models.Movies.movie_id == models.MovieDescriptions.fk_movie_id)\
        .filter(
            models.Movies.movie_id == movie_id
        ).first()
    if not db_object:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )
    if db_object[1]:
        db.delete(db_object[1])
        db.commit()
    db.delete(db_object[0])
    db.commit()
    if db_object[1] is None:
        fake_obj = {
            'score': 0,
            'movie_description_id': 0,
            'cast': 'invalid',
            'director': 'invalid',
            'synopsis': 'invalid'
            }
        return db_object[0].__dict__ | fake_obj
    return db_object[0].__dict__ | db_object[1].__dict__

def get_full_movie(movie_id: int, db: Session):
    db_object = db.query(models.Movies, models.MovieDescriptions)\
        .outerjoin(
            models.MovieDescriptions,
            models.Movies.movie_id == models.MovieDescriptions.fk_movie_id)\
        .filter(
            models.Movies.movie_id == movie_id
        ).first()
    if db_object is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )
    if db_object[1] is None:
        fake_obj = {
            'score': 0,
            'movie_description_id': 0,
            'cast': 'invalid',
            'director': 'invalid',
            'synopsis': 'invalid'
            }
        return db_object[0].__dict__ | fake_obj
    return db_object[0].__dict__ | db_object[1].__dict__


def update_movie(movie: ModifyMovies, db: Session):
    db_object = db.query(models.Movies)\
        .filter(models.Movies.movie_id == movie.movie_id)\
        .first()
    if not db_object:
        HTTPException(
            status_code=400,
            detail="Movie not found."
        )
    movie_dict = movie.__dict__
    if movie_dict.get('name', None) is not None:
        db_object.name = movie_dict['name']
    if movie_dict.get('launch_date', None) is not None:
        db_object.launch_date = movie_dict['launch_date']
    if movie_dict.get('fk_genre_id', None) is not None:
        db_object.fk_genre_id = movie_dict['fk_genre_id']
    db.commit()
    return db_object

def mod_movie_desc(movie: ModifyMovieDescription, db: Session):
    db_object = db.query(models.Movies, models.MovieDescriptions)\
        .outerjoin(
            models.MovieDescriptions,
            models.Movies.movie_id == models.MovieDescriptions.fk_movie_id)\
        .filter(
            models.Movies.movie_id == movie.movie_id
        ).first()
    if not db_object:
        raise HTTPException(
            status_code=404,
            detail="Movie not found."
        )
    if db_object[1] is None:
        if movie.__dict__.get('score', None) is None or\
                movie.__dict__.get('cast', None) is None or\
                movie.__dict__.get('director', None) is None or\
                movie.__dict__.get('synopsis', None) is None:
            raise HTTPException(
                status_code=422,
                detail="There is no description for this movie. You have to input all the items."
            )
        db_movie_description = models.MovieDescriptions(
            fk_movie_id=movie.movie_id,
            score=movie.score,
            cast=movie.cast,
            director=movie.director,
            synopsis=movie.synopsis
            )
        db.add(db_movie_description)
        db.commit()
        db.refresh(db_movie_description)
        return db_movie_description
    else:
        if movie.__dict__.get('score', None) is not None:
            db_object[1].score = movie.__dict__.get('score')
        if movie.__dict__.get('cast', None) is not None:
            db_object[1].cast = movie.__dict__.get('cast')
        if movie.__dict__.get('director', None) is not None:
            db_object[1].director = movie.__dict__.get('director')
        if movie.__dict__.get('synopsis', None) is not None:
            db_object[1].synopsis = movie.__dict__.get('synopsis')
        db.commit()
        db_object = db.query(models.Movies, models.MovieDescriptions)\
                    .outerjoin(
                        models.MovieDescriptions,
                        models.Movies.movie_id == models.MovieDescriptions.fk_movie_id)\
                    .filter(
                        models.Movies.movie_id == movie.movie_id
                    ).first()
    return db_object[1].__dict__
