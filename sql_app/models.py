from sqlalchemy import Boolean, Column, Integer, String

from sql_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class GenreType(Base):
    __tablename__ = "genre_types"

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)