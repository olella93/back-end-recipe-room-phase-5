from flask import Flask
from .extensions import db, migrate, jwt, ma, bcrypt, cors
from .config import Config
from .routes import init_routes

# Import models so they are available to migrations
from .models.user import User
from .models.recipe import Recipe
from .models.group import Group
from .models.group_member import GroupMember
from .models.rating import Rating

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004"], supports_credentials=True)

    # Register blueprints
    init_routes(app)

    return app
