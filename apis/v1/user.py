from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.crud import create_user, get_user_by_email, get_users
from app.database.db import Base, SessionLocal, engine
from app.database.schemas import User, UserCreate
from app.exceptions import APIException

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = APIRouter()


# create register user
@app.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            raise APIException(
                status_code=400,
                message="Email already registered"
            )
        return create_user(db=db, user=user)
    except APIException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
