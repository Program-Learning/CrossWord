from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.admin.routes import admin
    from app.player.routes import player
    from app.routes import index

    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(player, url_prefix='/player')

    return app
