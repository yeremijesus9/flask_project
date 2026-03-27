from flask import Blueprint, jsonify, request

from app.core.utils import success_response

bp = Blueprint('examples_modularization', __name__)

@bp.route("/")
def modularization_home():
        return """
            <body style="font-family: sans-serif; max-width: 820px; margin: 40px auto; line-height: 1.6; background: #fffdf6;">
                <a href="/examples-yeremi" style="color: #333;">← Volver al panel</a>
                <h1>Modularization Example</h1>
                <p>Este ejemplo quedo mas simple para que se vea mejor la idea de separar responsabilidades.</p>

                <div style="background: white; border: 1px solid #eadfcb; border-radius: 14px; padding: 20px;">
                    <h3 style="margin-top: 0;">Estructura</h3>
                    <pre style="margin: 0; white-space: pre-wrap;">modularization/
    |-- __init__.py
    |-- routes.py
    |-- users/
        |-- __init__.py
        |-- routes.py
        |-- user_service.py</pre>
                </div>

                <div style="background: #f8fbff; border: 1px solid #dce9f5; border-radius: 14px; padding: 20px; margin-top: 18px;">
                    <h3 style="margin-top: 0;">Flujo</h3>
                    <p><b>__init__.py</b> registra las rutas y prefijos para /modularization, <b>routes.py</b> gestiona la ruta visual ejemplos, y el package <b>users</b> separa las rutas de los datos.</p>
                    <p><a href="/examples-yeremi/modularization/users/">Abrir la parte visual del package users</a></p>
                </div>
            </body>
        """
