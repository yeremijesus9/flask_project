from flask import Blueprint
from app.api.basics.routes import bp

examples_german_bp = Blueprint('examples_german', __name__)

url_prefix = '/examples-german'

examples_german_bp.register_blueprint(bp, url_prefix=url_prefix)

__all__ = ['examples_german_bp']
