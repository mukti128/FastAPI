from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(225), nullable=False, unique=True)
    password_hash = Column(String(225), nullable=False)
    role = Column(String(10), nullable=False, default="student")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)