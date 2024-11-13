# app/database.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os


db = SQLAlchemy()


def setup_db(app):
    """Configura a conexão com o banco de dados."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///db.sqlite3'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def create_db(app):
    """Cria o banco de dados se ele não existir."""
    with app.app_context():
        db.create_all()