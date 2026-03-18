from flask import Flask

from .module_routes import register_example_blueprints


def create_app():
    app = Flask(__name__)
    register_example_blueprints(app)

    @app.route("/")
    def home():
        cards = [
            {
                "title": "Routes",
                "text": "Rutas basicas, parametros y query strings.",
                "href": "/examples/routes/",
                "color": "#ffe5d9",
            },
            {
                "title": "CRUD",
                "text": "Operaciones GET, POST, PUT y DELETE en memoria.",
                "href": "/examples/crud/",
                "color": "#d8f3dc",
            },
            {
                "title": "SQLite",
                "text": "Persistencia simple con una base de datos real.",
                "href": "/examples/sqlite/",
                "color": "#dceeff",
            },
            {
                "title": "Modularization",
                "text": "Ejemplo pequeno con package, service y routes.",
                "href": "/examples/modularization",
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
            <body style="font-family: sans-serif; max-width: 980px; margin: 40px auto; line-height: 1.5; background: #fcfcf7;">
                <h1>Panel de ejemplos Flask</h1>
                <p>Ahora no hace falta iniciar cada ejemplo por separado. Esta app registra varios <b>Blueprints</b> y te deja navegar todo desde un solo servidor.</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 24px;">
                    {cards_html}
                </div>
            </body>
        """

    @app.route("/examples/modularization")
    def modularization_home():
        return """
            <body style="font-family: sans-serif; max-width: 820px; margin: 40px auto; line-height: 1.6; background: #fffdf6;">
                <a href="/" style="color: #333;">← Volver al panel</a>
                <h1>Modularization Example</h1>
                <p>Este ejemplo quedo mas simple para que se vea mejor la idea de separar responsabilidades.</p>

                <div style="background: white; border: 1px solid #eadfcb; border-radius: 14px; padding: 20px;">
                    <h3 style="margin-top: 0;">Estructura</h3>
                    <pre style="margin: 0; white-space: pre-wrap;">modularization/
|-- app.py
|-- __init__.py
|-- module_routes.py
`-- users/
    |-- __init__.py
    |-- routes.py
    `-- user_service.py</pre>
                </div>

                <div style="background: #f8fbff; border: 1px solid #dce9f5; border-radius: 14px; padding: 20px; margin-top: 18px;">
                    <h3 style="margin-top: 0;">Flujo</h3>
                    <p><b>app.py</b> crea la aplicacion, <b>module_routes.py</b> registra ejemplos y el package <b>users</b> separa las rutas de los datos.</p>
                    <p><a href="/examples/modularization/users/">Abrir la parte visual del package users</a></p>
                </div>
            </body>
        """

    return app
