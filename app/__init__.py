from flask import Flask
from .extensions import db
from .routes import main
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-very-secret-key-here'  # Schimbă acest șir cu o cheie generată aleatoriu
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/carti.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inițializează extensiile
    db.init_app(app)
    migrate = Migrate(app, db)  # Inițializează Flask-Migrate

    # Înregistrează blueprint-ul
    app.register_blueprint(main)

    return app
