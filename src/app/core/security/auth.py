import jwt
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.repositories.user import get_user
from core.config import settings
from core.security.hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth:
    @staticmethod
    def authenticate_user(user_email: str, password: str, db: Session):
        user = get_user(user_email, db)
        if not user:
            return False
        if not Hasher.verify_password(password, user.password_hash):
            return False
        return user

    @staticmethod
    def generate_temporary_password(length=8):
        alphanumeric_characters = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphanumeric_characters) for i in range(length))

    @staticmethod
    def create_jwt_token(email: str, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = {"sub": email}
        if expires_delta:
            expire = datetime.now() + timedelta(minutes=150000)
        else:
            expire = datetime.now() + timedelta(minutes=150000)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_token.SECRET_KEY,
            algorithm=settings.jwt_token.ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        try:
            jwt.decode(
                jwt_token,
                settings.jwt_token.SECRET_KEY,
                algorithms=[settings.jwt_token.ALGORITHM],
            )
            return True
        except jwt.DecodeError:
            return False

    @staticmethod
    async def get_current_user(jwt_token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                jwt_token,
                settings.jwt_token.SECRET_KEY,
                algorithms=[settings.jwt_token.ALGORITHM],
            )
            user_email: str = payload.get("sub")
            if user_email is None:
                raise credentials_exception
        except jwt.JWTError:
            raise credentials_exception

        return user_email
