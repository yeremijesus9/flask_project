from flask import Blueprint
from app.api.examples_yeremi.sqlite.sqlites_examples import init_db, bp

init_db()

examples_sqlite_bp = Blueprint('examples_sqlite', __name__)

examples_sqlite_bp.register_blueprint(bp, url_prefix='/sqlite')

__all__ = ['init_db', 'examples_sqlite_bp']
