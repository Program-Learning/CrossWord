from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.set_password(password)
    def __repr__(self):
        return f'<Admin {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
    
    def modify(self, username: str=None, password: str=None):
        if username:
            self.username = username
        if password:
            self.set_password(password)