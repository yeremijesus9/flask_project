from flask import Blueprint
from app.api.examples_yeremi.modularization.routes import bp
from app.api.examples_yeremi.modularization.users import examples_users_bp

examples_modularization_bp = Blueprint('examples_modularization', __name__)

examples_modularization_bp.register_blueprint(bp, url_prefix='/modularization')
examples_modularization_bp.register_blueprint(examples_users_bp, url_prefix='/modularization')

__all__ = ['examples_modularization_bp']
