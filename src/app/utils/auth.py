import secrets
import string
from db.repositories.user import get_user
from utils.hashing import Hasher


class Auth:
    @staticmethod
    def authenticate_user(user, db):
        user_in_db = get_user(user.email, db)
        if not user:
            return False
        if not Hasher.verify_password(user.password, user_in_db.password_hash):
            return False
        return user

    @staticmethod
    def generate_temporary_password(length=8):
        alphanumeric_characters = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphanumeric_characters) for i in range(length))
