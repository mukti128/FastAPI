from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import create_access_token
from datetime import timedelta
import hashlib

# get password hash
def get_password_hash(password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    return sha256.hexdigest()

# create user
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

# user login
def user_login(db: Session, request: UserLogin):
    hashed_password = get_password_hash(request.password)
    user = db.query(User).filter(User.email == request.email).first()

    if not user or user.password_hash != hashed_password:
        return None
    
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_delta=access_token_expires
    )

    return {
        "userId": user.id,
        "username": user.username,
        "role": user.role,
        "token": access_token
    }

# get all user
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()