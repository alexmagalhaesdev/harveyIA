from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db_session
from schemas.user import UserLogin, UserCreate
from db.repositories.user import create_user, get_user
from pydantic import EmailStr
from core.security.auth import Auth
from utils.email import Email
from core.ui_config import templates

router = APIRouter()


@router.get("/signup", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def signup_get(request: Request):
    return templates.TemplateResponse("pages/signup.html", {"request": request})


@router.post(
    "/signup", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED
)
def signup_post(
    new_user: UserCreate,
    request: Request,
    db: Session = Depends(get_db_session),
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


@router.get("/login", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def login_get(
    request: Request,
):
    return templates.TemplateResponse("pages/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def login_post(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    authenticated_user = Auth.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token = Auth.create_jwt_token(form_data.username)
        response = templates.TemplateResponse(
            "pages/chat.html",
            {
                "request": request,
            },
        )
        print(f"MEU TOKEN {access_token}")
        response.set_cookie("Authorization", value=f"Bearer {access_token}")
        return response


@router.get(
    "/password_reset", response_class=HTMLResponse, status_code=status.HTTP_200_OK
)
def password_reset_get(request: Request):
    return templates.TemplateResponse("pages/password_reset.html", {"request": request})


@router.post(
    "/password_reset", response_class=HTMLResponse, status_code=status.HTTP_200_OK
)
def password_reset_post(
    user_email: EmailStr,
    request: Request,
    db: Session = Depends(get_db_session),
):
    user_in_db = get_user(user_email, db)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    temporary_password = Auth.generate_temporary_password()

    # reset_successful = update_user(user_in_db.id, {"password": temporary_password}, db)
    # if not reset_successful:
    #    raise HTTPException(
    #        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #        detail="Failed to reset password",
    #    )

    email_subject = "Temporary Password"
    email_text = f"Your temporary password is: {temporary_password}"
    Email.send_email(user_email, email_subject, email_text)

    return templates.TemplateResponse(
        "pages/password_reset_sent.html", {"request": request, "user_email": user_email}
    )
