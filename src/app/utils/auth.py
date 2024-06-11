from db.repositories.user import get_user
from utils.hashing import Hasher


class Auth:
    @staticmethod
    def authenticate_user(user, db):
        user_in_db = get_user(user.email, db)
        print(f"meu user {user_in_db}")
        if not user:
            return False
        if not Hasher.verify_password(user.password, user_in_db.password_hash):
            return False
        return user
