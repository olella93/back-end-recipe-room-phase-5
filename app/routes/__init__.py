from .auth_routes import auth_bp
from .recipe_routes import recipe_bp
from .group_routes import group_bp
from .comment_routes import comment_bp
from .bookmark_routes import bookmark_bp

def init_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipe_bp, url_prefix='/api')
    app.register_blueprint(group_bp, url_prefix='/api')
    app.register_blueprint(comment_bp)
    app.register_blueprint(bookmark_bp, url_prefix='/api')