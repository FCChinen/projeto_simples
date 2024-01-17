from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, Integer, String

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
    is_active = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


conexao = sqlite3.connect('./sql_app/sql_app.db')

cursor = conexao.cursor()

cursor.execute("INSERT INTO users (username, email, hashed_password, is_active) VALUES (?, ?, ?, ?)",
            ('felipechinen',
            'fcchinen@gmail.com',
            '9436a4a7d2912b886a2a8ba46ac9085773132d13eac8c39cee6870e74bb779e9',
            True))

conexao.commit()

conexao.close()
