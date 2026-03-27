from flask import Blueprint, Flask, jsonify, request

bp = Blueprint("crud_demo", __name__)

PRODUCTOS = [
    {"id": 1, "nombre": "Laptop", "precio": 3500},
    {"id": 2, "nombre": "Mouse", "precio": 80},
    {"id": 3, "nombre": "Teclado", "precio": 120},
]


def buscar_producto(producto_id):
    for producto in PRODUCTOS:
        if producto["id"] == producto_id:
            return producto
    return None


def construir_filas():
    filas = ""
    for producto in PRODUCTOS:
        filas += f"""
            <tr>
                <td>{producto["id"]}</td>
                <td>{producto["nombre"]}</td>
                <td>{producto["precio"]}</td>
            </tr>
        """
    return filas


def pagina_principal():
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
        <h1 class="titulo">CRUD</h1>
        <p class="subtitulo">Misma idea, poco código: crear, leer, actualizar y borrar.</p>

        <div class="grid">
            <div class="bloque c">Create<br><small>POST /productos</small></div>
            <div class="bloque r">Read<br><small>GET /productos</small></div>
            <div class="bloque u">Update<br><small>PUT /productos/1</small></div>
            <div class="bloque d">Delete<br><small>DELETE /productos/1</small></div>
        </div>

        <div class="card">
            <h3>Productos actuales</h3>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Precio</th>
                    </tr>
                </thead>
                <tbody>
                    {construir_filas()}
                </tbody>
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
    return pagina_principal()


@bp.route("/productos", methods=["GET"])
def listar_productos():
    return jsonify({"mensaje": "Lista de productos", "total": len(PRODUCTOS), "data": PRODUCTOS})


@bp.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto(producto_id):
    producto = buscar_producto(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto encontrado", "data": producto})


@bp.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json(silent=True) or {}
    nombre = datos.get("nombre")
    precio = datos.get("precio")

    if not nombre or precio is None:
        return jsonify({"error": "Debes enviar nombre y precio"}), 400

    nuevo = {
        "id": max((producto["id"] for producto in PRODUCTOS), default=0) + 1,
        "nombre": nombre,
        "precio": precio,
    }
    PRODUCTOS.append(nuevo)
    return jsonify({"mensaje": "Producto creado", "data": nuevo}), 201


@bp.route("/productos/<int:producto_id>", methods=["PUT"])
def actualizar_producto(producto_id):
    producto = buscar_producto(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    datos = request.get_json(silent=True) or {}
    producto["nombre"] = datos.get("nombre", producto["nombre"])
    producto["precio"] = datos.get("precio", producto["precio"])
    return jsonify({"mensaje": "Producto actualizado", "data": producto})


@bp.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    producto = buscar_producto(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    PRODUCTOS.remove(producto)
    return jsonify({"mensaje": "Producto eliminado", "data": producto})
