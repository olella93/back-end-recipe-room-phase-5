from flask import Flask
from .extensions import db, migrate, jwt, ma, bcrypt, cors
from .config import Config
from .routes import init_routes
from app.routes.recipe_routes import recipe_bp

# Import models so they are available to migrations
from .models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # Register blueprints
    init_routes(app)
    app.register_blueprint(recipe_bp, url_prefix="/api/recipes")

    return app
