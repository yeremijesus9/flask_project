import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from app.extensions import db, jwt, bcrypt
from app.config import config_by_name

load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'dev')
        
    # Configure Database and general settings from Config classes
    app.config.from_object(config_by_name[config_name])
    
    # Configure JWT Specifics (These could also go to config.py later)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False # True en producción con HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True # Activamos CSRF Protection via Cookies
    
    # Init Extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Import models explicitly so SQLAlchemy knows they exist
    from app.api.auth.models import User, TokenBlocklist
    
    # Import and register Blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp)
    
    # Setup JWT callbacks para Blocklisting (Logout)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    with app.app_context():
        db.create_all()

    @app.route('/')
    def hello_world():
        return jsonify(message='Server is running')
        
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        # Accessed only if a valid access_token is present in cookies/header
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return jsonify(
            msg="¡Accediste a una ruta segura verificando tokens!",
            user=user.username
        )

    return app
