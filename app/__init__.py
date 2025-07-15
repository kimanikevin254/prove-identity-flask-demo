from flask import Flask
from app.config import config
from app.api.routes import api_bp
from app.static_routes import static_bp

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(static_bp)

    return app