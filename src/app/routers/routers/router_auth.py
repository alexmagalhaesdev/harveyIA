from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db_session
from schemas.user import UserLogin, UserCreate
from db.repositories.user import create_user, update_user, get_user
from pydantic import EmailStr
from utils.auth import Auth
from utils.email import Email

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
def password_reset(user_email: EmailStr, db: Session = Depends(get_db_session)):
    user_in_db = get_user(user_email, db)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    temporary_password = Auth.generate_temporary_password()

    reset_successful = update_user(user_in_db.id, {"password": temporary_password}, db)
    if not reset_successful:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password",
        )

    email_subject = "Temporary Password"
    email_text = f"Your temporary password is: {temporary_password}"
    Email.send_email(user_email, email_subject, email_text)

    return {"message": "Password reset successful"}
