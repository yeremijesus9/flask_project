from flask import Blueprint, jsonify

from .user_service import get_summary, get_user_by_id, get_users


users_bp = Blueprint("users_demo", __name__)


@users_bp.route("/")
def users_home():
    cards = ""
    for user in get_users():
        cards += f"""
            <div style="background: {user['color']}; padding: 18px; border-radius: 14px;">
                <strong style="display: block; font-size: 18px;">{user['name']}</strong>
                <span>{user['role']}</span>
            </div>
        """

    return f"""
        <body style="font-family: sans-serif; max-width: 820px; margin: 40px auto; line-height: 1.5; background: #fffaf2;">
            <a href="/" style="color: #333;">← Volver al panel</a>
            <h1>Users Package</h1>
            <p>Este ejemplo separa datos y rutas en archivos distintos, pero de una forma pequeña y visual.</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 24px 0;">
                {cards}
            </div>

            <div style="background: white; border: 1px solid #e8dcc7; border-radius: 14px; padding: 18px;">
                <h3 style="margin-top: 0;">Prueba tambien</h3>
                <ul>
                    <li><a href="api">Ver todos los usuarios en JSON</a></li>
                    <li><a href="api/1">Ver el usuario 1 en JSON</a></li>
                    <li><a href="summary">Ver resumen del modulo</a></li>
                </ul>
            </div>
        </body>
    """


@users_bp.route("/api")
def users_api():
    return jsonify({"module": "users", "data": get_users()})


@users_bp.route("/api/<int:user_id>")
def user_detail(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"data": user})


@users_bp.route("/summary")
def summary():
    return jsonify(get_summary())
