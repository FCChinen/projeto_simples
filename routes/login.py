from fastapi import HTTPException, status
from models.login_request import UserInDB
from typing import Dict, Annotated
import datetime
import jwt


with open('./pem_files/secret.txt', 'r') as f:
    SECRET_KEY = f.read()
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def get_db_users() -> Dict:
# TODO: Implementar acesso a banco
    return {
        "felipechinen": {
            "username": "felipechinen",
            "name": "Felipe Chinen",
            "email": "fcchinen@gmwail.com",
            "hashed_password": "fakehashpwd",
            "status": False
            }
    }


def hash_password(password: str):
    return "fakehash" + password


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
    

def get_access_token(login: str, password: str):
    user_dict = get_db_users().get(login)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
    user = UserInDB(**user_dict)
    hashed_password = hash_password(password)
    if user.hashed_password != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    print("passou por aqui")
    return {
        "access_token": create_access_token(user),
        "token_type": "bearer"
    }