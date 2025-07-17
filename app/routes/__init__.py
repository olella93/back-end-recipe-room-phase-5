from .auth_routes import auth_bp
from .recipe_routes import recipe_bp
from .group_routes import group_bp
from ..main import main_bp 

def init_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix = '/api/auth')
    app.register_blueprint(recipe_bp, url_prefix = '/api')
    app.register_blueprint(group_bp, url_prefix = '/api')
