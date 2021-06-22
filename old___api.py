import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    res = {
        'success': True,
    }
    return jsonify(res), 200

@app.route('/add_pet', methods=['POST'])
def add_pet():
    req = request.json

    if req != None:
        res = {
            'success': True,
            'message': 'es string'
        }
        return jsonify(res), 200
    res = {
        'success': False,
        'message': 'No se puede procesar solicitud'
    }
    return jsonify(res), 400

app.run()