from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicijalizacija SQLAlchemy objekta
db = SQLAlchemy()

def create_app():
    # Kreiranje Flask aplikacije
    app = Flask(__name__)

    # Učitavanje konfiguracije iz config.py
    app.config.from_object('config')

    # Inicijalizacija baze s aplikacijom
    db.init_app(app)

    # Registracija blueprint-a
    from .routes import main
    app.register_blueprint(main)

    return app
