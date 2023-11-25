import os
import psycopg2
from flask import g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host="localhost",
            database="catalog",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
