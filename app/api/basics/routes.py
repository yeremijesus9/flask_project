from flask import Blueprint, jsonify, render_template
from .Cochecito import animacion
from .LetrasDeColores import animacion_letras
from .RelojDigital import animacion_reloj
from .Suma import suma

bp = Blueprint('basics', __name__)

@bp.route('/')
def hello_world():
    return render_template('basics/home.html')

@bp.route('/animacion-coche')
def animation_coche():
    return animacion()

@bp.route('/animacion-letras')
def animation_letras():
    return animacion_letras()

@bp.route('/animacion-reloj')
def animation_reloj():
    return animacion_reloj()

@bp.route('/suma')
def sum():
    return suma()