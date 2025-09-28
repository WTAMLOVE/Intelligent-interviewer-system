from extensions import db
from models.user import User
from utils.security import hash_password, check_password


def create_user(username, email, password, role="interviewee"):
    # Disallow creation of admin users via public registration
    if role == "admin":
        raise ValueError("Cannot create admin user via registration")

    pw = hash_password(password)
    user = User(username=username, email=email, password_hash=pw, role=role)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    if not check_password(password, user.password_hash):
        return None
    return user
