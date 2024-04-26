from flask import Flask
from .extensions import db
from .routes import main
from flask_migrate import Migrate
from .naive_bayes_api import naive_bayes_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-very-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/carti.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(main)
    app.register_blueprint(naive_bayes_blueprint, url_prefix='/naive_bayes')

    return app
