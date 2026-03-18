"""
Centraliza todos los blueprints que queremos mostrar
desde una sola aplicacion principal.
"""

from ..crud import crud_bp
from ..routes import routes_bp
from ..sqlite import init_db, sqlite_bp
from .users import users_bp


EXAMPLE_BLUEPRINTS = (
    (users_bp, "/examples/modularization/users"),
    (routes_bp, "/examples/routes"),
    (crud_bp, "/examples/crud"),
    (sqlite_bp, "/examples/sqlite"),
)


def register_example_blueprints(app):
    init_db()

    for blueprint, prefix in EXAMPLE_BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=prefix)


__all__ = ["EXAMPLE_BLUEPRINTS", "register_example_blueprints"]
