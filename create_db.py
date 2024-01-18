from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, Integer, String, Date, DECIMAL, ForeignKey

from sqlalchemy.orm import relationship

import sqlite3


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
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


Base.metadata.create_all(bind=engine)

conexao = sqlite3.connect('./sql_app/sql_app.db')

cursor = conexao.cursor()

cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
            ('felipechinen',
            'fcchinen@gmail.com',
            '9436a4a7d2912b886a2a8ba46ac9085773132d13eac8c39cee6870e74bb779e9'))

cursor.execute("INSERT INTO genre_types (genre_name) VALUES ('invalid_genre')")

conexao.commit()

conexao.close()
