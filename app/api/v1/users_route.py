from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.crud.user_crud import create_user, get_users
from app.core.database import get_db

router = APIRouter()

@router.post(
    "/", 
    response_model=UserResponse,
    responses={
        400: {"description": "Username or email already registered"},
        500: {"description": "Internal server error"}
    }
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or email already registered"
        )
    return create_user(db, user)
    
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)