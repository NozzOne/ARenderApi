from fastapi import APIRouter

from .v1 import v1

root = APIRouter()
root.include_router(v1, prefix="/v1", tags=["v1"])
