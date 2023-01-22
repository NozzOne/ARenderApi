from datetime import datetime
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.processing import ImageProcessing
from app.database.db import Base, SessionLocal, engine
from app.exceptions import APIException


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


render = APIRouter()


class RenderQueryParams:
    def __init__(self,
                 image: str = Query(
                     ..., description="The image to process, can be a url or base64 string"),
                 base64: bool = Query(
                     False, description="Return the image as base64"),
                 ) -> None:
        self.image = ImageProcessing(image)
        self.base64 = base64


@render.post("/render")
async def render_image(
    params: RenderQueryParams = Depends(),
    db: Session = Depends(get_db),
):
    try:
        result = params.image.to_base64
        if params.base64:
            result = "data:image/png;base64," + result

        return {
            "data": {
                "image": result,
            }
        }
    except APIException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )