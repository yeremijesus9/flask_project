from flask import Blueprint, jsonify, request

from app.core.utils import success_response

bp = Blueprint('examples_yeremi', __name__)

@bp.route("/")
def home():
        cards = [
            {
                "title": "Routes",
                "text": "Rutas basicas, parametros y query strings.",
                "href": "/examples-yeremi/routes",
                "color": "#ffe5d9",
            },
            {
                "title": "CRUD",
                "text": "Operaciones GET, POST, PUT y DELETE en memoria.",
                "href": "/examples-yeremi/crud",
                "color": "#d8f3dc",
            },
            {
                "title": "SQLite",
                "text": "Persistencia simple con una base de datos real.",
                "href": "/examples-yeremi/sqlite",
                "color": "#dceeff",
            },
            {
                "title": "Modularization",
                "text": "Ejemplo pequeno con package, service y routes.",
                "href": "/examples-yeremi/modularization",
                "color": "#fff1b6",
            },
        ]

        cards_html = ""
        for card in cards:
            cards_html += f"""
                <a href="{card['href']}" style="text-decoration: none; color: #222;">
                    <div style="background: {card['color']}; padding: 20px; border-radius: 18px; min-height: 130px;">
                        <strong style="display: block; font-size: 20px; margin-bottom: 10px;">{card['title']}</strong>
                        <span>{card['text']}</span>
                    </div>
                </a>
            """

        return f"""
        <a href="/" style="color: #333;">← Volver al inicio</a>
            <body style="font-family: sans-serif; max-width: 980px; margin: 40px auto; line-height: 1.5; background: #fcfcf7;">
                <h1>Panel de ejemplos Flask</h1>
                <p>Ahora no hace falta iniciar cada ejemplo por separado. Esta app registra varios <b>Blueprints</b> y te deja navegar todo desde un solo servidor.</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 24px;">
                    {cards_html}
                </div>
            </body>
        """
