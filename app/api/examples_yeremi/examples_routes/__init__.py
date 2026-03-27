from flask import Blueprint
from app.api.examples_yeremi.examples_routes.routes import bp

examples_routes_bp = Blueprint('examples_routes', __name__)
examples_routes_bp.register_blueprint(bp, url_prefix='/routes')

__all__ = ['examples_routes_bp']
