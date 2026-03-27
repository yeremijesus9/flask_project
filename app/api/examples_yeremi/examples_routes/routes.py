from flask import Blueprint, jsonify, request

from app.core.utils import success_response

bp = Blueprint('examples_routes', __name__)

PRODUCTS_DATA = {
    1: {"name": "Laptop", "price": 999.99},
    2: {"name": "Mouse", "price": 25.50},
    3: {"name": "Keyboard", "price": 45.00},
}


@bp.route("/")
def home():
    return """
        <body style="font-family: sans-serif; max-width: 820px; margin: 40px auto; line-height: 1.6; background: #fffaf8;">
            <a href="/examples-yeremi" style="color: #333;">← Volver al panel</a>
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
                <pre style="background: #222; color: #fff; padding: 14px; border-radius: 10px;">POST /examples-yeremi/routes/students
{
  "name": "Lucia"
}</pre>
            </div>
        </body>
    """


@bp.route("/hello")
def hello():
    return success_response(message="Hola desde una ruta simple")


@bp.route("/user/<name>")
def user(name):
    return success_response(message=f"Hola, {name}")


@bp.route("/product/<int:product_id>")
def product(product_id):
    product_data = PRODUCTS_DATA.get(product_id)
    if not product_data:
        return success_response(message="Producto no encontrado", status_code=404)
    return success_response(data={"id": product_id, "product": product_data})


@bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "GET":
        return success_response(data={
            "students": [
                {"id": 1, "name": "Yeremi"},
                {"id": 2, "name": "German"},
            ]
        })
    
    data = request.get_json() or {}
    return success_response(data=data, message="Estudiante creado", status_code=201)


@bp.route("/search")
def search():
    term = request.args.get("q", "sin termino")
    return success_response(data={"search": term})
