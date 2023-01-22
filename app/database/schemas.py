from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


DefaultModel = {
    "status": bool,
    "system": {
        "code": int,
        "message": str
    },
    "source": List[User],
    "timestemp": int
}