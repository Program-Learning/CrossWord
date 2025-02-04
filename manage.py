from app import create_app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from config import Config

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)


@cli.command("init", help="Initialize the database.")
def init_db():
    db.create_all()
    print("Initialized the database.")
    add_admin()
    print("Added admin user.")
    add_player()
    print("Added common user.")
    Config.init_app(app)
    print("Initialized the config for the app.")


@cli.command("reinit", help="ReInitialize the database.")
def reinit_db():
    db.drop_all()
    print("Dropped all tables.")
    db.create_all()
    print("ReInitialized the database.")
    add_admin()
    print("Added admin user.")
    add_player()
    print("Added common user.")
    Config.init_app(app)
    print("Initialized the config for the app.")


def add_player(username: str = "Anonymous", password: str = "Anonymous"):
    from app.player.models import Player

    player = Player(username, password)
    db.session.add(player)
    db.session.commit()


def add_admin(username: str = "root", password: str = "root"):
    from app.admin.models import Admin

    admin = Admin(username, password)
    db.session.add(admin)
    db.session.commit()


@cli.command("add_common_player", help="Add common player.")
def add_player_cli():
    return add_player


@cli.command("add_admin", help="Add admin user.")
def add_admin_cli():
    return add_admin


if __name__ == "__main__":
    cli()
