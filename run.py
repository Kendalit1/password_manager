from app import app, db
from app.models.user import User
import os

def create_db_if_not_exists():
    db_path = os.path.join(os.getcwd(), 'site.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()

            print("[+] База данных создана")
    else:
        print("[ℹ] База уже существует")

if __name__ == '__main__':
    create_db_if_not_exists()
    app.run(debug=True)
