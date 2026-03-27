import sqlite3
from pathlib import Path

from flask import Blueprint, Flask, jsonify, request

bp = Blueprint("sqlite_demo", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
DB_PATH = BASE_DIR / "instance" / "project.sqlite"
PRODUCTOS_INICIALES_SQLITE = [
    ("Camara Web", 210),
    ("Auriculares", 450),
    ("Microfono USB", 690),
]


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
            """
        )

        total = conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
        if total == 0:
            conn.executemany(
                "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
                PRODUCTOS_INICIALES_SQLITE,
            )
            return

        # Si la base tenia los datos viejos del CRUD, los cambiamos
        # por los de SQLite para diferenciar ambos ejemplos.
        nombres_actuales = [
            fila[0]
            for fila in conn.execute(
                "SELECT nombre FROM productos ORDER BY id"
            ).fetchall()
        ]
        if nombres_actuales == ["Laptop", "Mouse", "Teclado"]:
            conn.execute("DELETE FROM productos")
            conn.executemany(
                "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
                PRODUCTOS_INICIALES_SQLITE,
            )


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def filas_html(productos):
    filas = ""
    for producto in productos:
        filas += f"""
            <tr>
                <td>{producto["id"]}</td>
                <td>{producto["nombre"]}</td>
                <td>{producto["precio"]}</td>
            </tr>
        """
    return filas


def pagina_principal(productos):
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: sans-serif;
                max-width: 920px;
                margin: 32px auto;
                background: #f7fafc;
                color: #1f2937;
            }}
            .titulo {{
                margin-bottom: 8px;
            }}
            .subtitulo {{
                margin-top: 0;
                color: #475569;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 12px;
                margin: 18px 0;
            }}
            .bloque {{
                border-radius: 12px;
                padding: 14px;
                font-weight: 700;
            }}
            .c {{ background: #d9f99d; }}
            .r {{ background: #bfdbfe; }}
            .u {{ background: #fde68a; }}
            .d {{ background: #fecaca; }}
            .card {{
                background: white;
                border: 1px solid #dbe4ee;
                border-radius: 14px;
                padding: 16px;
                margin-top: 14px;
            }}
            .zona-demo {{
                display: grid;
                gap: 10px;
            }}
            .fila {{
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                align-items: center;
            }}
            input {{
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 10px;
            }}
            button {{
                border: 0;
                border-radius: 8px;
                padding: 8px 12px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                text-align: left;
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }}
            th {{
                background: #f1f5f9;
            }}
            pre {{
                background: #0f172a;
                color: #e2e8f0;
                padding: 12px;
                border-radius: 10px;
                overflow-x: auto;
            }}
            a {{
                color: #1d4ed8;
            }}
        </style>
    </head>
    <body>
        <a href="/examples-yeremi">Volver al panel</a>
        <h1 class="titulo">SQLite</h1>
        <p class="subtitulo">Es igual al CRUD, pero aqui usamos productos distintos para identificar rapido que es base de datos real.</p>

        <div class="grid">
            <div class="bloque c">Create<br><small>POST /productos</small></div>
            <div class="bloque r">Read<br><small>GET /productos</small></div>
            <div class="bloque u">Update<br><small>PUT /productos/1</small></div>
            <div class="bloque d">Delete<br><small>DELETE /productos/1</small></div>
        </div>

        <div class="card">
            <h3>Productos guardados en SQLite</h3>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Precio</th>
                    </tr>
                </thead>
                <tbody>{filas_html(productos)}</tbody>
            </table>
        </div>

        <div class="card">
            <h3>Rutas para probar</h3>
            <ul>
                <li><b>GET</b> <a href="productos">/productos</a></li>
                <li><b>GET</b> <a href="productos/1">/productos/1</a></li>
                <li><b>POST</b> /productos</li>
                <li><b>PUT</b> /productos/1</li>
                <li><b>DELETE</b> /productos/1</li>
            </ul>
            <p>JSON para POST o PUT:</p>
            <pre>{{
  "nombre": "Monitor",
  "precio": 799
}}</pre>
        </div>

        <div class="card">
            <h3>Prueba aqui mismo (funcional)</h3>
            <div class="zona-demo">
                <form id="form-crear" class="fila">
                    <b>POST</b>
                    <input id="crear-nombre" placeholder="nombre" required />
                    <input id="crear-precio" type="number" placeholder="precio" required />
                    <button type="submit">Crear</button>
                </form>

                <form id="form-actualizar" class="fila">
                    <b>PUT</b>
                    <input id="act-id" type="number" placeholder="id" required />
                    <input id="act-nombre" placeholder="nombre" required />
                    <input id="act-precio" type="number" placeholder="precio" required />
                    <button type="submit">Actualizar</button>
                </form>

                <form id="form-eliminar" class="fila">
                    <b>DELETE</b>
                    <input id="del-id" type="number" placeholder="id" required />
                    <button type="submit" style="background:#dc2626;">Eliminar</button>
                </form>
            </div>
            <p>Respuesta API:</p>
            <pre id="salida-api">Aqui veras el resultado en JSON.</pre>
        </div>

        <script>
            async function llamarApi(url, metodo, data) {{
                const opciones = {{
                    method: metodo,
                    headers: {{"Content-Type": "application/json"}}
                }};

                if (data) {{
                    opciones.body = JSON.stringify(data);
                }}

                const resp = await fetch(url, opciones);
                const json = await resp.json();
                document.getElementById("salida-api").textContent = JSON.stringify(json, null, 2);

                if (resp.ok) {{
                    setTimeout(function () {{
                        window.location.reload();
                    }}, 700);
                }}
            }}

            document.getElementById("form-crear").addEventListener("submit", function (e) {{
                e.preventDefault();
                const nombre = document.getElementById("crear-nombre").value;
                const precio = Number(document.getElementById("crear-precio").value);
                llamarApi("productos", "POST", {{nombre: nombre, precio: precio}});
            }});

            document.getElementById("form-actualizar").addEventListener("submit", function (e) {{
                e.preventDefault();
                const id = document.getElementById("act-id").value;
                const nombre = document.getElementById("act-nombre").value;
                const precio = Number(document.getElementById("act-precio").value);
                llamarApi("productos/" + id, "PUT", {{nombre: nombre, precio: precio}});
            }});

            document.getElementById("form-eliminar").addEventListener("submit", function (e) {{
                e.preventDefault();
                const id = document.getElementById("del-id").value;
                llamarApi("productos/" + id, "DELETE");
            }});
        </script>
    </body>
    </html>
    """


@bp.route("/")
def inicio():
    conn = get_conn()
    productos = conn.execute("SELECT * FROM productos ORDER BY id").fetchall()
    conn.close()
    return pagina_principal(productos)


@bp.route("/productos", methods=["GET"])
def listar_productos():
    conn = get_conn()
    productos = conn.execute("SELECT * FROM productos ORDER BY id").fetchall()
    conn.close()
    return jsonify(
        {
            "mensaje": "Lista de productos",
            "total": len(productos),
            "data": [dict(p) for p in productos],
        }
    )


@bp.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto(producto_id):
    conn = get_conn()
    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?",
        (producto_id,),
    ).fetchone()
    conn.close()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto encontrado", "data": dict(producto)})


@bp.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json(silent=True) or {}
    nombre = datos.get("nombre")
    precio = datos.get("precio")

    if not nombre or precio is None:
        return jsonify({"error": "Debes enviar nombre y precio"}), 400

    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
        (nombre, precio),
    )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Producto creado", "data": {"id": cursor.lastrowid, "nombre": nombre, "precio": precio}}), 201


@bp.route("/productos/<int:producto_id>", methods=["PUT"])
def actualizar_producto(producto_id):
    datos = request.get_json(silent=True) or {}

    conn = get_conn()
    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?",
        (producto_id,),
    ).fetchone()

    if not producto:
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    nombre = datos.get("nombre", producto["nombre"])
    precio = datos.get("precio", producto["precio"])
    conn.execute(
        "UPDATE productos SET nombre = ?, precio = ? WHERE id = ?",
        (nombre, precio, producto_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Producto actualizado", "data": {"id": producto_id, "nombre": nombre, "precio": precio}})


@bp.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    conn = get_conn()
    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?",
        (producto_id,),
    ).fetchone()

    if not producto:
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    conn.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Producto eliminado", "data": dict(producto)})
