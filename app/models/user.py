from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    passwords = db.relationship('Password', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"
