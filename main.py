import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes.login import get_access_token, check_access_token
from sqlalchemy.orm import Session

from sql_app.database import SessionLocal, engine
import sql_app.models
import sql_app.schemas
import sql_app.crud

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


@app.post("/users/",
          tags=["user management"],
          response_model=sql_app.schemas.User,
          dependencies=[Depends(verify_token)])
def create_user(user: sql_app.schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = sql_app.crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return sql_app.crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[sql_app.schemas.User],
         tags=["user management"],
         dependencies=[Depends(verify_token)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = sql_app.crud.get_users(db, skip=skip, limit=limit)
    for user in users:
        print(user.__dict__)
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)