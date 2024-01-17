import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes.login import get_access_token, check_access_token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def verify_token(token: str = Depends(oauth2_scheme)):
    if not check_access_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@app.post("/token")
async def auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return get_access_token(form_data.username, form_data.password)


@app.get("/", dependencies=[Depends(verify_token)])
async def hello_world():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)