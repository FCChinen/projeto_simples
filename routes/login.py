from fastapi import HTTPException
from models.login_request import UserInDB
from sqlalchemy.orm import Session
import datetime
import jwt
from common import hash_password
from sql_app.crud import get_user_by_username


with open('./pem_files/secret.txt', 'r') as f:
    SECRET_KEY = f.read()
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: UserInDB):
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    info = data.model_dump()
    info.update({"exp": expire})
    return jwt.encode(info, SECRET_KEY, algorithm="HS256")


def check_access_token(token: str) -> str:
    try:
        info = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return info
    except Exception as e:
        print(e)


def get_access_token(db: Session, username: str, password: str):
    user_dict = get_user_by_username(db=db, username=username)
    if not user_dict:
        raise HTTPException(status_code=400,
                            detail="Invalid username or password")
    user_dict = user_dict.__dict__
    print(user_dict)
    user = UserInDB(**user_dict)
    hashed_password = hash_password(password)
    if user.hashed_password != hashed_password:
        raise HTTPException(status_code=400,
                            detail="Invalid username or password")
    print("passou por aqui")
    return {
        "access_token": create_access_token(user),
        "token_type": "bearer"
    }
