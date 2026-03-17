"""
=======================================================
  FLASK - METODOS CRUD
=======================================================

CRUD significa:
    C = Create   -> Crear
    R = Read     -> Leer
    U = Update   -> Actualizar
    D = Delete   -> Eliminar

En este ejemplo usamos una lista en memoria para que el
comportamiento sea facil de entender sin base de datos.
Cuando reinicias el servidor, los datos vuelven al estado
inicial.
=======================================================
"""

from flask import Flask, jsonify, request


app = Flask(__name__)


# "Base de datos" temporal en memoria
productos = [
    {"id": 1, "nombre": "Laptop", "precio": 3500},
    {"id": 2, "nombre": "Mouse", "precio": 80},
    {"id": 3, "nombre": "Teclado", "precio": 120},
]


def buscar_producto(producto_id):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None


@app.route("/")
def inicio():
    return """
        <body style="font-family: sans-serif; max-width: 850px; margin: 40px auto; line-height: 1.6;">
            <h1>Ejemplo CRUD con Python Flask</h1>
            <p>Este ejemplo muestra como crear una API sencilla con los metodos <b>GET, POST, PUT y DELETE</b>.</p>

            <div style="background: #f4f4f4; padding: 20px; border-radius: 8px;">
                <h3>Rutas disponibles</h3>
                <ul>
                    <li><b>GET</b> /productos</li>
                    <li><b>GET</b> /productos/1</li>
                    <li><b>POST</b> /productos</li>
                    <li><b>PUT</b> /productos/1</li>
                    <li><b>DELETE</b> /productos/1</li>
                </ul>
            </div>

            <div style="margin-top: 24px;">
                <h3>Ejemplo de JSON para POST o PUT</h3>
                <pre style="background: #222; color: #fff; padding: 16px; border-radius: 8px; overflow-x: auto;">
{
    "nombre": "Monitor",
    "precio": 799
}
                </pre>
            </div>
        </body>
    """


# -------------------------------------------------------
# READ - LISTAR TODOS LOS PRODUCTOS
# -------------------------------------------------------
@app.route("/productos", methods=["GET"])
def listar_productos():
    return jsonify(
        {
            "mensaje": "Lista de productos",
            "total": len(productos),
            "data": productos,
        }
    )


# -------------------------------------------------------
# READ - OBTENER UN PRODUCTO POR ID
# -------------------------------------------------------
@app.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto(producto_id):
    producto = buscar_producto(producto_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto encontrado", "data": producto})


# -------------------------------------------------------
# CREATE - CREAR UN PRODUCTO
# -------------------------------------------------------
@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Debes enviar un JSON en el cuerpo de la peticion"}), 400

    nombre = datos.get("nombre")
    precio = datos.get("precio")

    if not nombre or precio is None:
        return jsonify({"error": "Los campos 'nombre' y 'precio' son obligatorios"}), 400

    nuevo_id = max((producto["id"] for producto in productos), default=0) + 1
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
    }
    productos.append(nuevo_producto)

    return (
        jsonify(
            {
                "mensaje": "Producto creado correctamente",
                "data": nuevo_producto,
            }
        ),
        201,
    )


# -------------------------------------------------------
# UPDATE - ACTUALIZAR UN PRODUCTO
# -------------------------------------------------------
@app.route("/productos/<int:producto_id>", methods=["PUT"])
def actualizar_producto(producto_id):
    producto = buscar_producto(producto_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Debes enviar un JSON en el cuerpo de la peticion"}), 400

    if "nombre" in datos:
        producto["nombre"] = datos["nombre"]

    if "precio" in datos:
        producto["precio"] = datos["precio"]

    return jsonify(
        {
            "mensaje": "Producto actualizado correctamente",
            "data": producto,
        }
    )


# -------------------------------------------------------
# DELETE - ELIMINAR UN PRODUCTO
# -------------------------------------------------------
@app.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    producto = buscar_producto(producto_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    productos.remove(producto)

    return jsonify(
        {
            "mensaje": "Producto eliminado correctamente",
            "data": producto,
        }
    )


if __name__ == "__main__":
    print("\n✅ Servidor CRUD arrancado en http://127.0.0.1:5003")
    app.run(debug=True, port=5003)
