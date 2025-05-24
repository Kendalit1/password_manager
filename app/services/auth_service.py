from app import db
from app.models.user import User
from app.utils.security import hash_password, check_password

def register_user(email, raw_password):
    existing = User.query.filter_by(email=email).first()
    if existing:
        return None
    hashed = hash_password(raw_password)
    user = User(email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, raw_password):
    user = User.query.filter_by(email=email).first()
    if user and check_password(raw_password, user.password_hash):
        return user
    return None
