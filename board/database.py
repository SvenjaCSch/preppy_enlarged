import sqlite3
import click
from flask import current_app, g
from typing import Any

def init_app(app):
    """
    close old database before starting new one
    Argument:
        app
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command("init-db")
def init_db_command()->None:
    """
    initializsing database
    Argument:
        str: "init-db"
    """
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))
    click.echo("You successfully initialized the database!")

def get_db()->Any:
    """
    connect to SLQite database
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["SQLALCHEMY_DATABASE_URI"].replace('sqlite:///', 'instance/'),
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=Any)->None:
    """
    close database
    Argument:
        Any: e
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
