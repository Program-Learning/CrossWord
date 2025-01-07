from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username: str, password: str, name: str="", id_card_number: str=""):
        self.username = username
        self.name = name
        self.set_password(password)
    def __repr__(self):
        return f'<Player {self.username}>'
    def to_dict(self):
        return {
            'player_id': self.player_id,
            'username': self.username,
            'name': self.name,
        }
    def modify(self, username: str=None, name: str=None, password: str=None):
        if username:
            self.username = username

        if name:
            self.name = name
            
        if password:
            self.set_password(password)