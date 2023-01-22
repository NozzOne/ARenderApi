from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class AuthUser(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"AuthUser(username={self.username}, password={self.password})"


class AuthUserToken(Base):
    __tablename__ = "auth_user_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    token = Column(String, unique=True, index=True)

    user = relationship("AuthUser", back_populates="tokens")

    def __repr__(self):
        return f"AuthUserToken(user_id={self.user_id}, token={self.token})"