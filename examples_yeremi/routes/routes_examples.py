"""
=======================================================
  FLASK - DECORADORES ROUTER (RUTAS)
=======================================================

¿Qué es un decorador en Flask?
--------------------------------
Un decorador en Flask es una función especial que "envuelve" otra función
para registrarla como manejador de una URL concreta.

El decorador más usado es @app.route(), que le dice a Flask:
"Cuando alguien visite ESTA URL, ejecuta ESTA función".

Estructura básica:
    @app.route('/ruta')
    def nombre_funcion():
        return 'Respuesta'

=======================================================
"""

from flask import Flask, jsonify, request


app = Flask(__name__)


# -------------------------------------------------------
# 1. RUTA BÁSICA (GET por defecto)
# -------------------------------------------------------
# El decorador @app.route('/') registra la función 'inicio'
# para que responda cuando alguien visite la raíz del sitio.

@app.route('/')
def inicio():
    return '<h1>Bienvenido a la API de Rutas Flask</h1>'


# -------------------------------------------------------
# 2. RUTA CON UNA URL PERSONALIZADA
# -------------------------------------------------------
# Podemos definir cualquier URL, no solo la raíz.

@app.route('/saludo')
def saludo():
    return jsonify({
        'mensaje': '¡Hola desde Flask!',
        'descripcion': 'Esta es una ruta personalizada'
    })


# -------------------------------------------------------
# 3. RUTAS CON PARÁMETROS DINÁMICOS
# -------------------------------------------------------
# Flask permite capturar partes de la URL como variables.
# Sintaxis: <nombre_variable>

@app.route('/usuario/<nombre>')
def saludar_usuario(nombre):
    return jsonify({
        'mensaje': f'Hola, {nombre}!',
        'descripcion': 'El nombre fue capturado desde la URL'
    })


# -------------------------------------------------------
# 4. PARÁMETROS CON TIPO DE DATO ESPECIFICADO
# -------------------------------------------------------
# Flask puede convertir automáticamente el tipo del parámetro.
# Tipos disponibles: string (default), int, float, path, uuid

@app.route('/producto/<int:producto_id>')
def obtener_producto(producto_id):
    # Si el id no es un número entero, Flask devuelve 404 automáticamente
    productos = {
        1: {'nombre': 'Laptop', 'precio': 999.99},
        2: {'nombre': 'Mouse',  'precio': 25.50},
        3: {'nombre': 'Teclado', 'precio': 45.00},
    }

    producto = productos.get(producto_id)

    if producto:
        return jsonify({'id': producto_id, 'producto': producto})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404


# -------------------------------------------------------
# 5. RUTA CON MÚLTIPLES PARÁMETROS
# -------------------------------------------------------

@app.route('/categoria/<string:categoria>/item/<int:item_id>')
def obtener_item(categoria, item_id):
    return jsonify({
        'categoria': categoria,
        'item_id': item_id,
        'mensaje': f'Item {item_id} de la categoría "{categoria}"'
    })


# -------------------------------------------------------
# 6. RUTA CON MÉTODOS HTTP (GET, POST, PUT, DELETE)
# -------------------------------------------------------
# Por defecto Flask solo acepta GET.
# Con el parámetro 'methods' indicamos qué métodos acepta la ruta.

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'GET':
        # Devolver lista de alumnos
        alumnos_lista = [
            {'id': 1, 'nombre': 'Yeremi', 'nota': 9.5},
            {'id': 2, 'nombre': 'German', 'nota': 8.0},
        ]
        return jsonify({'alumnos': alumnos_lista})

    elif request.method == 'POST':
        # Recibir datos en JSON y "añadir" un alumno
        datos = request.get_json()
        return jsonify({
            'mensaje': 'Alumno recibido correctamente',
            'alumno_recibido': datos
        }), 201  # 201 = Created


@app.route('/alumnos/<int:alumno_id>', methods=['GET', 'PUT', 'DELETE'])
def alumno_por_id(alumno_id):
    if request.method == 'GET':
        return jsonify({'id': alumno_id, 'nombre': 'Yeremi', 'nota': 9.5})

    elif request.method == 'PUT':
        datos = request.get_json()
        return jsonify({
            'mensaje': f'Alumno {alumno_id} actualizado',
            'datos_nuevos': datos
        })

    elif request.method == 'DELETE':
        return jsonify({'mensaje': f'Alumno {alumno_id} eliminado correctamente'})


# -------------------------------------------------------
# 7. MÚLTIPLES URLs PARA LA MISMA FUNCIÓN
# -------------------------------------------------------
# Podemos apuntar varias rutas a la misma función usando
# varios decoradores @app.route() apilados.

@app.route('/info')
@app.route('/informacion')
@app.route('/acerca-de')
def informacion():
    return jsonify({
        'proyecto': 'Investigación Flask',
        'tema': 'Decoradores Router',
        'autor': 'Yeremi',
        'rutas_equivalentes': ['/info', '/informacion', '/acerca-de']
    })


# -------------------------------------------------------
# 8. RUTA CON PARÁMETRO DE TIPO PATH
# -------------------------------------------------------
# El tipo 'path' acepta barras (/) dentro del parámetro,
# útil para capturar rutas de archivos o subdirectorios.

@app.route('/archivo/<path:ruta_archivo>')
def leer_archivo(ruta_archivo):
    return jsonify({
        'ruta_capturada': ruta_archivo,
        'descripcion': 'El tipo <path> permite capturar barras /'
    })


# -------------------------------------------------------
# 9. QUERY PARAMETERS (parámetros en la URL ?clave=valor)
# -------------------------------------------------------
# Estos no van en el decorador, se leen con request.args

@app.route('/buscar')
def buscar():
    termino = request.args.get('q', 'sin término')       # ?q=algo
    limite  = request.args.get('limite', 10, type=int)   # ?limite=5
    return jsonify({
        'busqueda': termino,
        'limite': limite,
        'ejemplo_url': '/buscar?q=flask&limite=5'
    })


# -------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5001)
