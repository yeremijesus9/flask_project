
def animacion():
    return """
    <style>
        body { background-color: #1a1a1a; overflow: hidden; margin: 0; }
        .coche {
            font-size: 80px;
            position: absolute;
            top: 50%;
            white-space: nowrap;
            animation: conducir 5s linear infinite;
        }
        @keyframes conducir {
            0% { right: -150px; transform: translateY(-50%) scaleX(1); }
            49% { transform: translateY(-50%) scaleX(1); }
            50% { right: 100%; transform: translateY(-50%) scaleX(-1); }
            99% { transform: translateY(-50%) scaleX(-1); }
            100% { right: -150px; transform: translateY(-50%) scaleX(1); }
        }
        .carretera {
            position: absolute;
            top: 60%;
            width: 400%;
            height: 20px;
            background: dashed #555;
        }
    </style>
    <div class="carretera"></div>
    <div class="coche">🚗💨</div>
    """
