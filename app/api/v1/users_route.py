from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, LoginResponse
from app.crud.user_crud import create_user, get_users, user_login
from app.core.database import get_db
from app.core.security import get_current_user, bearer_scheme
from app.core.token_store import add_to_blacklist

router = APIRouter()

#register user
@router.post(
    "/register", 
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User registered successfully."},
        400: {"description": "Username or email already registered"},
        422: {"description": "Validation error"}
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
    
    create_user(db, user)
    return {"message": "User registered successfully."}
    
#login user
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid email or password"},
        422: {"description": "Validation error"},
    }
)
def login(request: UserLogin, db: Session = Depends(get_db)):
    result = user_login(db, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return {
        "message": "Login successful",
        "data": result
    }

#logout user
@router.post(
        "/logout",
        status_code=status.HTTP_200_OK
)
def logout(token: str = Depends(bearer_scheme), user: dict = Depends(get_current_user)):
    add_to_blacklist(token.credentials)
    return {"message": "Logout successful."}

#get all user
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)