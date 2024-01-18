from sqlalchemy import Boolean, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from sql_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class GenreType(Base):
    __tablename__ = "genre_types"

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)

    movies = relationship('Movies', back_populates='genre_types', uselist=False)


class Movies(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    launch_date = Column(Date)

    fk_genre_id = Column(Integer, ForeignKey('genre_types.genre_id'))

    genre_types = relationship('GenreType', back_populates="movies", single_parent=True, foreign_keys=[fk_genre_id])

    movie_parent = relationship("MovieDescriptions",
                                back_populates="movie_description",
                                uselist=False)


class MovieDescriptions(Base):
    __tablename__ = "movie_descriptions"

    movie_description_id = Column(Integer, primary_key=True)
    fk_movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    score = Column(DECIMAL)
    cast = Column(String)
    director = Column(String)
    synopsis = Column(String)

    movie_description = relationship(
        "Movies",
        back_populates="movie_parent",
        single_parent=True,
        foreign_keys=[fk_movie_id]
    )