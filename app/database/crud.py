from sqlalchemy.orm import Session

from app.database import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.AuthUser).filter(models.AuthUser.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.AuthUser).filter(models.AuthUser.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.AuthUser).filter(models.AuthUser.email == email).first()

def get_user_by_token(db: Session, token: str):
    return db.query(models.AuthUser).filter(models.AuthUser.token == token).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AuthUser).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.AuthUser(username=user.username, email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_token(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.AuthUser(username=user.username, email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.AuthUser(username=user.username, email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user