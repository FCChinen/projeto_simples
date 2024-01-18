import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes.login import get_access_token, check_access_token
from routes.genre_type import insert_genre_type, get_genre_types, delete_genre_types, update_genre_types
from routes.movies import add_movie
from sqlalchemy.orm import Session

from models.genre_type_response import GenreType
from models.movies import MovieDescription, Movies

from sql_app.database import SessionLocal, engine
import sql_app.models
import sql_app.schemas
import routes.user

sql_app.models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def verify_token(token: str = Depends(oauth2_scheme)):
    if not check_access_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@app.post("/token",
          tags=["auth"])
async def auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
               db: Session = Depends(get_db)):
    return get_access_token(db=db,
                            username=form_data.username,
                            password=form_data.password)


@app.post("/users",
          tags=["user management"],
          response_model=sql_app.schemas.User,
          dependencies=[Depends(verify_token)])
async def create_user(user: sql_app.schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = routes.user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return routes.user.create_user(db=db, user=user)


@app.get("/users",
         response_model=list[sql_app.schemas.User],
         tags=["user management"],
         dependencies=[Depends(verify_token)])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = routes.user.get_users(db, skip=skip, limit=limit)
    for user in users:
        print(user.__dict__)
    return users


@app.get("/genre_type",
        response_model=list[GenreType],
        tags=["genre management"],
        dependencies=[Depends(verify_token)])
async def add_genre(skip: int = 0,
                    limit: int = 10,
                    db: Session = Depends(get_db)):
    return get_genre_types(db=db, skip=skip, limit=limit)


@app.post("/genre_type",
          response_model=GenreType,
          tags=["genre management"],
          dependencies=[Depends(verify_token)])
async def add_genre(genre_name: str, db: Session = Depends(get_db)):
    return insert_genre_type(db=db, genre_name=genre_name)


@app.delete("/genre_type",
            response_model=list[GenreType],
            tags=["genre management"],
            dependencies=[Depends(verify_token)])
async def delete_genre(genre_id: int | None = None,
                       genre_name: str | None = None,
                       db: Session = Depends(get_db)):
    if genre_id is None and genre_name is None:
        raise HTTPException(
            status_code=422,
            detail="Either genre_name or genre_id must be not null"
        )
    return delete_genre_types(genre_id, genre_name, db)


@app.put("/genre_type",
            response_model=GenreType,
            tags=["genre management"],
            dependencies=[Depends(verify_token)])
async def update_genre(genre_id: int,
                       genre_name: str,
                       db: Session = Depends(get_db)):
    return update_genre_types(genre_id, genre_name, db)

@app.post("/movie",
          response_model=Movies,
          tags=["movie management"],
          dependencies=[Depends(verify_token)])
async def add_movies(movie: Movies,
                       db: Session = Depends(get_db)):
    return add_movie(movie, db)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)