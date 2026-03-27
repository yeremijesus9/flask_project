from flask import Blueprint
from app.api.examples_yeremi.routes import bp
from app.api.examples_yeremi.crud import examples_crud_bp
from app.api.examples_yeremi.examples_routes import examples_routes_bp
from app.api.examples_yeremi.sqlite import examples_sqlite_bp
from app.api.examples_yeremi.modularization import examples_modularization_bp

examples_yeremi_bp = Blueprint('examples_yeremi', __name__)

url_prefix = '/examples-yeremi'

examples_yeremi_bp.register_blueprint(bp, url_prefix='/examples-yeremi')
examples_yeremi_bp.register_blueprint(examples_crud_bp, url_prefix=url_prefix)
examples_yeremi_bp.register_blueprint(examples_routes_bp, url_prefix=url_prefix)
examples_yeremi_bp.register_blueprint(examples_sqlite_bp, url_prefix=url_prefix)
examples_yeremi_bp.register_blueprint(examples_modularization_bp, url_prefix=url_prefix)

__all__ = ['examples_yeremi_bp']
