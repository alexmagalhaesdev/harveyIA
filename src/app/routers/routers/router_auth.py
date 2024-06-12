from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db_session
from schemas.user import UserLogin, UserCreate
from db.repositories.user import create_user, update_user, get_user
from pydantic import EmailStr
from utils.auth import Auth
from utils.email import Email

router = APIRouter()


@router.get("/signup", response_model=HTMLResponse, status_code=status.HTTP_200_OK)
def signup_get(
    templates: Jinja2Templates = Depends(),
    request: Request = Depends(),
):
    return templates.TemplateResponse("pages/signup.html", {"request": request})


@router.post(
    "/signup", response_model=HTMLResponse, status_code=status.HTTP_201_CREATED
)
def signup_post(
    new_user: UserCreate,
    db: Session = Depends(get_db_session),
    templates: Jinja2Templates = Depends(),
    request: Request = Depends(),
):
    created_user = create_user(new_user, db)
    if not created_user:
        # If there was an error in creating the user, display an error message on the same page
        error_message = "Error creating user. Please try again."
        return templates.TemplateResponse(
            "pages/signup.html", {"request": request, "error_message": error_message}
        )
    else:
        # If the user was successfully created, redirect to another page
        return RedirectResponse(url="/chat")


@router.get("/signup", response_model=HTMLResponse, status_code=status.HTTP_200_OK)
def login_get(
    templates: Jinja2Templates = Depends(),
    request: Request = Depends(),
):
    return templates.TemplateResponse("pages/login.html", {"request": request})


@router.post("/login", status_code=status.HTTP_200_OK)
def login_post(
    user: UserLogin,
    db: Session = Depends(get_db_session),
    templates: Jinja2Templates = Depends(),
    request: Request = Depends(),
):
    authenticated_user = Auth.authenticate_user(user, db)
    if not authenticated_user:
        # If authentication fails, redirect to the login page with an error message
        error_message = "Invalid username or password"
        return templates.TemplateResponse(
            "pages/login.html", {"request": request, "error_message": error_message}
        )
    else:
        # If authentication succeeds, redirect to another page
        return RedirectResponse(url="/chat")


@router.get(
    "/password_reset", response_class=HTMLResponse, status_code=status.HTTP_200_OK
)
def password_reset_get(request: Request, templates: Jinja2Templates = Depends()):
    return templates.TemplateResponse("pages/password_reset.html", {"request": request})


@router.post(
    "/password_reset", response_class=HTMLResponse, status_code=status.HTTP_200_OK
)
def password_reset_post(
    user_email: EmailStr,
    db: Session = Depends(get_db_session),
    templates: Jinja2Templates = Depends(),
    request: Request = Depends(),
):
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

    return templates.TemplateResponse(
        "pages/password_reset_sent.html", {"request": request, "user_email": user_email}
    )
