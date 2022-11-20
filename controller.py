from flask import Blueprint, request
from typing import Optional
import service
import model

bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'

@bp.route('/sign-in', methods=['POST'])
def sign_in():
    student = model.Student(**request.get_json())
    response = service.sign_in(student)
    return response

@bp.route('/sign-up', methods=['POST'])
def sign_up():
    student = request.get_json()
    response = service.sign_up(student)
    return response
