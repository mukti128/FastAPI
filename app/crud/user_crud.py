from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
import hashlib

def get_password_hash(password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    return sha256.hexdigest()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()