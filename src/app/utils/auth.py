from db.repositories.user import get_user
from utils.hashing import Hasher


class Auth:
    @staticmethod
    def authenticate_user(user, db):
        user = get_user(user.email, db)
        if not user:
            return False
        if not Hasher.verify_password(user.password, user.password_hash):
            return False
        return user
