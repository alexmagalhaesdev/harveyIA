from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from db.models.user import User
from core.security.hashing import Hasher


def create_user(user: UserCreate, db: Session):
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=Hasher.get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user


def get_user(email: str, db: Session):
    user_in_db = db.query(User).filter(User.email == email).first()

    return user_in_db


def update_user(id: int, user: UserUpdate, db: Session):
    user_in_db = db.query(User).filter(User.id == id).first()

    if not user_in_db:
        return False

    for field, value in user.dict(exclude_unset=True).items():
        setattr(user_in_db, field, value)

    db.commit()
    return user_in_db


def delete_user(id: int, db: Session):
    user_in_db = db.query(User).filter(User.id == id)

    if not user_in_db.first():
        return {"error": f"Could not find user with id {id}"}

    user_in_db.delete()
    db.commit()

    return {"message": f"Deleted user with id {id}"}
