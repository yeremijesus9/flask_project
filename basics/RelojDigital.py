from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/animacion-reloj')
def animacion():
    return """
    <style>
        body { 
            background-color: #121212; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
            overflow: hidden; 
            font-family: 'Courier New', Courier, monospace;
        }
        .reloj {
            font-size: 80px;
            font-weight: bold;
            color: #00ff41; /* Color estilo Matrix/Terminal */
            text-shadow: 0 0 20px #00ff41;
            animation: pulso 2s infinite;
        }
        @keyframes pulso {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
    </style>
    
    <div id="reloj" class="reloj">00:00:00</div>

    <script>
        function actualizarReloj() {
            const ahora = new Date();
            const horas = String(ahora.getHours()).padStart(2, '0');
            const minutos = String(ahora.getMinutes()).padStart(2, '0');
            const segundos = String(ahora.getSeconds()).padStart(2, '0');
            document.getElementById('reloj').textContent = `${horas}:${minutos}:${segundos}`;
        }
        setInterval(actualizarReloj, 1000);
        actualizarReloj(); // Ejecución inmediata al cargar
    </script>
    """

if __name__ == '__main__':
    app.run(debug=True)
