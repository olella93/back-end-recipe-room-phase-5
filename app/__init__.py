from flask import Flask
from flask_migrate import Migrate 

from .config import Config
from .db import init_db
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    migrate = Migrate(app, db) 
    init_routes(app)

    return app
