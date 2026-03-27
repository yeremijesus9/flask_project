from flask import Blueprint
from app.api.examples_yeremi.modularization.users.routes import bp

examples_users_bp = Blueprint('examples_users', __name__)

examples_users_bp.register_blueprint(bp, url_prefix='/users')

__all__ = ['examples_users_bp']