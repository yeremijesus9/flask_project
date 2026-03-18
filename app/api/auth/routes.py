from flask import Blueprint, request
from app.api.auth.services import AuthService
from app.core.utils import success_response, error_response
from app.core.exceptions import APIException
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)

# Blueprint prefix will be handled on register in app.__init__.py
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return error_response("Missing field", status_code=400)

    try:
        AuthService.register_user(data['username'], data['email'], data['password'])
        return success_response(message="Usuario registrado exitosamente", status_code=201)
    except APIException as e:
        return error_response(e.message, status_code=e.status_code)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return error_response("Faltan credenciales", status_code=400)

    user = AuthService.verify_credentials(data['username'], data['password'])
    
    if user:
        access_token, refresh_token = AuthService.generate_tokens(user.id)
        
        # Como se decidió en la revision, las respuestas web usan HttpOnly Cookies
        resp, code = success_response(data={'login': True}, message="Login exitoso")
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, code

    return error_response("Credenciales inválidas", status_code=401)

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    AuthService.revoke_token(jti)
    
    resp, code = success_response(message="Logout exitoso")
    unset_jwt_cookies(resp)
    return resp, code

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    current_refresh_jti = get_jwt()["jti"]
    
    # Revocar viejo token
    AuthService.revoke_token(current_refresh_jti)
    
    # Generar nuevos
    new_access_token, new_refresh_token = AuthService.generate_tokens(current_user_id)
    
    resp, code = success_response(message="Tokens refrescados por rotación activa")
    set_access_cookies(resp, new_access_token)
    set_refresh_cookies(resp, new_refresh_token)
    
    return resp, code
