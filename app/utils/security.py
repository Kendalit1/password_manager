from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password: str, hash: str) -> bool:
    return bcrypt.check_password_hash(hash, password)
