from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from config import Config

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.car_routes import car_bp
    from .routes.rental_routes import rental_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(car_bp, url_prefix='/cars')
    app.register_blueprint(rental_bp, url_prefix='/rentals')

    return app
