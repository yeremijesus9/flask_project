from flask import Blueprint, jsonify

# Creamos un Blueprint (un "plano" de rutas)
# 'usuarios' es el nombre interno del blueprint
# __name__ ayuda a Flask a localizar recursos
usuarios_bp = Blueprint('usuarios', __name__)

# NOTA: Aquí usamos @usuarios_bp.route en lugar de @app.route
# Esto permite que este archivo no dependa de que la 'app' esté creada aquí.

@usuarios_bp.route('/')
def listar_usuarios():
    return jsonify({
        "modulo": "Usuarios",
        "lista": ["Yeremi", "German", "yoandres"],
        "mensaje": "Este decorador viene de un Blueprint"
    })

@usuarios_bp.route('/<int:id>')
def obtener_detalle(id):
    return jsonify({
        "id": id,
        "nombre": "Usuario " + str(id),
        "info": "Ruta modularizada"
    })
