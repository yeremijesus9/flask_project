from flask import Flask
from rutas_modulares import usuarios_bp

app = Flask(__name__)

app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

@app.route('/')
def inicio():
    return """
        <body style="font-family: sans-serif; max-width: 600px; margin: 40px auto; line-height: 1.6;">
            <h1> Ejemplo de Modularización</h1>
            <p>Este ejemplo demuestra cómo separar las rutas en diferentes archivos usando <b>Blueprints</b>.</p>
            <div style="background: #f4f4f4; padding: 20px; border-radius: 8px;">
                <h3>Enlaces de prueba:</h3>
                <ul>
                    <li><a href="/usuarios/">Ver lista de usuarios (JSON)</a></li>
                    <li><a href="/usuarios/123">Ver detalle de usuario (Dinámico)</a></li>
                </ul>
            </div>
        </body>
    """

if __name__ == '__main__':
    print("\n✅ Servidor modular arrancado en http://127.0.0.1:5002")
    app.run(debug=True, port=5002)
