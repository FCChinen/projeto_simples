from sqlalchemy.orm import Session
import sql_app.models as models
import sql_app.schemas as schemas
from common import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email,
                          username=user.username,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_object = db.query(models.User)\
                    .filter(models.User.id == user_id)\
                    .first()
    if not db_object:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db.delete(db_object)
    db.commit()
    return db_object.__dict__

def update_user(db: Session, user: schemas.UpdateUser):
    db_object = db.query(models.User)\
                .filter(models.User.id == user.id)\
                .first()
    if not db_object:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.__dict__.get('email', None) is not None:
        db_object.email = user.__dict__.get('email')
    if user.__dict__.get('username', None) is not None:
        db_object.username = user.__dict__.get('username')
    if user.__dict__.get('password', None) is not None:
        db_object.hashed_password = hash_password(user.__dict__.get('password'))
    db.commit()
    return db_object
