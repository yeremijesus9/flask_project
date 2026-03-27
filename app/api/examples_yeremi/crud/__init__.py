from flask import Blueprint
from app.api.examples_yeremi.crud.crud_examples import bp

examples_crud_bp = Blueprint('examples_crud', __name__)

examples_crud_bp.register_blueprint(bp, url_prefix='/crud')

__all__ = ['examples_crud_bp']
