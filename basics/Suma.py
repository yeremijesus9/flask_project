from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/suma')
def suma():
    resultado = 35 + 5
    return "<h1>35 + 5 = {}</h1>".format(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=True)