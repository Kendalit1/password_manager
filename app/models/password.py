from app import db

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    entropy = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Password {self.value}>"
