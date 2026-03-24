from flask import Flask 

app = Flask(__name__)

@app.route('/')
def hello_world() -> str:
    return "<h1>Hello, World!</h1>"

@app.route('/otraruta')
def otro_nombre() -> str:
    return "<h1>Cualquier Cosa!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=True)