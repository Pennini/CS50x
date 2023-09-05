from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import query_sql

app = Flask(__name__)

DATABASE = "history.db"


@app.route("/")
def index():
    rows = ex("SELECT * FROM users")

    print(rows)

    return "<p>Hello, World!</p>"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def ex(query, *args):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(query, args)

    if query.split(" ")[0] == "SELECT":
        rows = cursor.fetchall()
        return rows
    else:
        db.commit()


if __name__ == "__main__":
    app.run()
