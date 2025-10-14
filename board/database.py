import sqlite3
import click
from flask import current_app, g
from typing import Any
import json

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

def add_vector_ref(db, upload_id: int, vector_id: str, chunk_index: int = 0, metadata: dict | None = None):
    """
    Fügt einen neuen Eintrag in vector_refs hinzu
    """
    db.execute(
        "INSERT INTO vector_refs (upload_id, vector_id, chunk_index, metadata) VALUES (?, ?, ?, ?)",
        (upload_id, vector_id, chunk_index, json.dumps(metadata) if metadata else None)
    )
    db.commit()


def get_vectors_for_upload(db, upload_id: int):
    """
    Holt alle vector_id-Einträge zu einem bestimmten Upload
    """
    return db.execute(
        "SELECT vector_id FROM vector_refs WHERE upload_id = ?",
        (upload_id,)
    ).fetchall()


def delete_vectors_for_upload(db, upload_id: int, chroma_client):
    """
    Löscht alle Vektoren in Chroma und die Referenzen in SQLite
    """
    vectors = get_vectors_for_upload(db, upload_id)
    for v in vectors:
        chroma_client.delete(ids=[v["vector_id"]])
    db.execute("DELETE FROM vector_refs WHERE upload_id = ?", (upload_id,))
    db.commit()

#db = Chroma(persist_directory=f"./vector_db/{user_id}", embedding_function=embeddings)

"""
# Nach dem Einfügen eines Dokuments in Chroma
vector_id = chroma.add_embedding(vector, metadata={"page":1})
cursor.execute(
    "INSERT INTO vector_refs (upload_id, vector_id, chunk_index) VALUES (?, ?, ?)",
    (upload_id, vector_id, chunk_index)
)
conn.commit()

# Alle Embeddings eines Dokuments löschen
cursor.execute("SELECT vector_id FROM vector_refs WHERE upload_id=?", (upload_id,))
for vector_id in cursor.fetchall():
    chroma.delete_embedding(vector_id)
"""