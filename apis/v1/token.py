# endpoint for token generation

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.crud import create_user_token, get_user_by_token
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

token = APIRouter()



