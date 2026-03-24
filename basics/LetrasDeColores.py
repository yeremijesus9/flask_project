from flask import Flask

app = Flask(__name__)

@app.route('/animacion-letras')
def animacion():
    return """
    <style>
        body { background-color: #121212; overflow: hidden; }
        .letras {
            font-size: 50px;
            font-weight: bold;
            position: absolute;
            width: 100%;
            text-align: center;
            animation: subirBajar 3s ease-in-out infinite;
        }
        @keyframes subirBajar {
            0%, 100% { top: 10%; color: #ff5733; }
            50% { top: 80%; color: #33ff57; }
        }
    </style>
    <div class="letras">¡ESTOY EN MOVIMIENTO!</div>
    """

if __name__ == '__main__':
    app.run(debug=True)