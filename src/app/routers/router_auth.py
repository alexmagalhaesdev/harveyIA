from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db_session
from schemas.user import UserLogin, UserCreate
from db.repositories.user import create_user, update_user
from utils.auth import Auth

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db_session)):
    created_user = create_user(user, db)
    return created_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db_session)):
    authenticated_user = Auth.authenticate_user(user, db)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return {"message": "Login successful"}


@router.post("/password_reset", status_code=status.HTTP_200_OK)
def password_reset(
    email: str, new_password: str, db: Session = Depends(get_db_session)
):
    reset_successful = update_user(email, new_password, db)
    if not reset_successful:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "Password reset successful"}
