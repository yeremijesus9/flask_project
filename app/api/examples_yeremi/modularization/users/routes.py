from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from .services import UserService

bp = Blueprint("users_demo", __name__)

@bp.route("/")
def users_home():
    cards = ""
    for user in UserService.get_users():
        cards += f"""
            <div style="background: {user['color']}; padding: 18px; border-radius: 14px;">
                <strong style="display: block; font-size: 18px;">{user['name']}</strong>
                <span>{user['role']}</span>
            </div>
        """

    return f"""
        <body style="font-family: sans-serif; max-width: 820px; margin: 40px auto; line-height: 1.5; background: #fffaf2;">
            <a href="/examples-yeremi/modularization" style="color: #333;">← Volver al panel</a>
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

@bp.route("/api")
def users_api():
    return jsonify({"module": "users", "data": UserService.get_users()})

@bp.route("/api/<int:user_id>")
def user_detail(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"data": user})

@bp.route("/summary")
def summary():
    return jsonify(UserService.get_summary())

@bp.route("/api", methods=["POST"])
@jwt_required()
def create_user():
    data = request.get_json()
    required_fields = ["user_id", "name", "role", "color"]
    
    if not data:
        return error_response("No data provided", status_code=400)
    
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response(f"Missing fields: {', '.join(missing)}", status_code=400)
    
    try:
        user = UserService.create_user(
            user_id=data["user_id"],
            name=data["name"],
            role=data["role"],
            color=data["color"]
        )
        return success_response(data=user, message="User created", status_code=201)
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)
    except ValueError as e:
        return error_response(str(e), status_code=400)

@bp.route("/api/<int:profile_id>", methods=["PUT"])
@jwt_required()
def update_user(profile_id):
    data = request.get_json()
    
    if not data:
        return error_response("No data provided", status_code=400)
    
    user = UserService.update_user(profile_id, data)
    
    if not user:
        return error_response("User not found", status_code=404)
    
    return success_response(data=user, message="User updated")

@bp.route("/api/<int:profile_id>", methods=["DELETE"])
@jwt_required()
def delete_user(profile_id):
    result = UserService.delete_user(profile_id)
    
    if not result:
        return error_response("User not found", status_code=404)
    
    return success_response(message="User deleted")

@bp.route("/api/by-user/<int:user_id>")
@jwt_required()
def user_by_user_id(user_id):
    user = UserService.get_user_by_user_id(user_id)
    
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return jsonify({"data": user})
