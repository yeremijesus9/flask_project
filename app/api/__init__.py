from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import modules and register them to the main API blueprint
from app.api.auth.routes import bp as auth_bp
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
