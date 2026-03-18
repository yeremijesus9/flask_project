"""
=======================================================
  FLASK + SQLITE - CRUD CON BASE DE DATOS REAL
=======================================================

En este ejemplo ya no usamos una lista en memoria. Ahora los 
datos se guardan en un archivo llamado 'inventario.db'.

Si cierras el servidor, ¡tus productos seguirán ahí!
=======================================================
"""

import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "inventario.db"


def init_db():
    """Crea la tabla si no existe al arrancar la app."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
            """
        )
    print("✅ Base de datos inicializada")


def dict_factory(cursor, row):
    """Convierte las filas de la DB en diccionarios para jsonify."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection():
    """Abre una conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = dict_factory  # Esto permite acceder por nombre: producto['nombre']
    return conn


@app.route("/")
def inicio():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos ORDER BY id").fetchall()
    conn.close()

    filas_html = ""
    for producto in productos:
        filas_html += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{producto['id']}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{producto['nombre']}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{producto['precio']}</td>
            </tr>
        """

    if not filas_html:
        filas_html = """
            <tr>
                <td colspan="3" style="padding: 16px; text-align: center; color: #6b7280;">
                    No hay productos guardados todavía.
                </td>
            </tr>
        """

    return f"""
        <body style="font-family: sans-serif; max-width: 850px; margin: 40px auto; line-height: 1.6; background: #f0f4f8;">
            <h1 style="color: #2c3e50;">SQLite + Flask: CRUD Persistente</h1>
            <p>Los datos ahora se guardan en <b>inventario.db</b>.</p>

            <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 24px;">
                <h3 style="margin-top: 0;">Productos guardados</h3>
                <table style="width: 100%; border-collapse: collapse; background: #ffffff;">
                    <thead>
                        <tr style="background: #eef2f7; text-align: left;">
                            <th style="padding: 12px;">ID</th>
                            <th style="padding: 12px;">Nombre</th>
                            <th style="padding: 12px;">Precio</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_html}
                    </tbody>
                </table>
            </div>

            <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0;">Rutas de la API</h3>
                <code style="display: block; background: #2d3436; color: #fab1a0; padding: 15px; border-radius: 8px;">
                    GET    /productos          -> Listar todos<br>
                    GET    /productos/&lt;id&gt;     -> Buscar uno<br>
                    POST   /productos          -> Crear (enviar JSON)<br>
                    PUT    /productos/&lt;id&gt;     -> Editar<br>
                    DELETE /productos/&lt;id&gt;     -> Borrar
                </code>
            </div>
        </body>
    """


# -------------------------------------------------------
# READ - LISTAR TODOS
# -------------------------------------------------------
@app.route("/productos", methods=["GET"])
def listar_productos():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()

    return jsonify(
        {
            "mensaje": "Productos desde SQLite",
            "total": len(productos),
            "data": productos,
        }
    )


# -------------------------------------------------------
# READ - OBTENER UNO
# -------------------------------------------------------
@app.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto(producto_id):
    conn = get_db_connection()
    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?", (producto_id,)
    ).fetchone()
    conn.close()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"data": producto})


# -------------------------------------------------------
# CREATE - INSERTAR EN DB
# -------------------------------------------------------
@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json(silent=True)
    if not datos or "nombre" not in datos or "precio" not in datos:
        return jsonify({"error": "Faltan datos (nombre, precio)"}), 400

    nombre = datos["nombre"]
    precio = datos["precio"]

    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return (
        jsonify(
            {
                "mensaje": "Guardado en SQLite!",
                "data": {"id": nuevo_id, "nombre": nombre, "precio": precio},
            }
        ),
        201,
    )


# -------------------------------------------------------
# UPDATE - ACTUALIZAR FILA
# -------------------------------------------------------
@app.route("/productos/<int:producto_id>", methods=["PUT"])
def actualizar_producto(producto_id):
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "JSON requerido"}), 400

    conn = get_db_connection()
    # Verificamos si existe
    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?", (producto_id,)
    ).fetchone()

    if not producto:
        conn.close()
        return jsonify({"error": "No existe ese producto"}), 404

    # Solo actualizamos los campos que vengan en el JSON
    nombre = datos.get("nombre", producto["nombre"])
    precio = datos.get("precio", producto["precio"])

    conn.execute(
        "UPDATE productos SET nombre = ?, precio = ? WHERE id = ?",
        (nombre, precio, producto_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Producto actualizado", "id": producto_id})


# -------------------------------------------------------
# DELETE - ELIMINAR FILA
# -------------------------------------------------------
@app.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()

    filas_afectadas = cursor.rowcount
    conn.close()

    if filas_afectadas == 0:
        return jsonify({"error": "No se encontró el producto para borrar"}), 404

    return jsonify({"mensaje": "Producto eliminado de la base de datos"})


if __name__ == "__main__":
    init_db()  # Importante: Crea la tabla al iniciar
    print("\n🚀 Servidor SQLite arrancado en http://127.0.0.1:5004")
    app.run(debug=True, port=5004)
