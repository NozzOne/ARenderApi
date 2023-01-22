from fastapi import APIRouter

from app.database.db import Base, SessionLocal, engine

from .render import render

v1 = APIRouter()

v1.include_router(render)