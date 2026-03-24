from flask import Blueprint, Flask, jsonify, request


routes_bp = Blueprint("routes_demo", __name__)

PRODUCTS = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Mouse", "price": 25.50},
    3: {"name": "Keyboard", "price": 45.00},
}


@routes_bp.route("/")
def home():
    return """
        <body style="font-family: sans-serif; max-width: 820px; margin: 40px auto; line-height: 1.6; background: #fffaf8;">
            <a href="/" style="color: #333;">← Volver al panel</a>
            <h1>Ejemplo de Rutas</h1>
            <p>Esta pagina junta los tipos de rutas mas utiles en una vista pequena y visual.</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
                <a href="hello" style="background: #ffe8d6; padding: 16px; border-radius: 14px; text-decoration: none; color: #222;">Ruta simple: <b>/hello</b></a>
                <a href="user/Ana" style="background: #d8f3dc; padding: 16px; border-radius: 14px; text-decoration: none; color: #222;">Parametro dinamico: <b>/user/Ana</b></a>
                <a href="product/2" style="background: #dceeff; padding: 16px; border-radius: 14px; text-decoration: none; color: #222;">Parametro tipado: <b>/product/2</b></a>
                <a href="search?q=flask" style="background: #fff1b6; padding: 16px; border-radius: 14px; text-decoration: none; color: #222;">Query string: <b>/search?q=flask</b></a>
            </div>

            <div style="background: white; border: 1px solid #eadfcb; border-radius: 14px; padding: 18px; margin-top: 18px;">
                <h3 style="margin-top: 0;">Extra</h3>
                <p>La ruta <b>/students</b> acepta <b>GET</b> y <b>POST</b>.</p>
                <pre style="background: #222; color: #fff; padding: 14px; border-radius: 10px;">POST /examples/routes/students
{
  "name": "Lucia"
}</pre>
            </div>
        </body>
    """


@routes_bp.route("/hello")
def hello():
    return jsonify({"message": "Hola desde una ruta simple"})


@routes_bp.route("/user/<name>")
def user(name):
    return jsonify({"message": f"Hola, {name}"})


@routes_bp.route("/product/<int:product_id>")
def product(product_id):
    product_data = PRODUCTS.get(product_id)

    if not product_data:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"id": product_id, "product": product_data})


@routes_bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "GET":
        return jsonify(
            {
                "students": [
                    {"id": 1, "name": "Yeremi"},
                    {"id": 2, "name": "German"},
                ]
            }
        )

    data = request.get_json(silent=True) or {}
    return jsonify({"created": data}), 201


@routes_bp.route("/search")
def search():
    term = request.args.get("q", "sin termino")
    return jsonify({"search": term})


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    print("\n✅ Servidor de rutas en http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
