from flask import Blueprint, request, make_response
from typing import Optional
import service
import model
import json
import exceptions

bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'

@bp.route('/exception', methods=['GET'])
def exception():
    response = make_response()
    e = exceptions.StudentAlreadyExistsError()
    response.data = json.dumps({
        'error': {
            e.__class__.__name__: e.message
        }
    })
    response.status = e.status
    return response

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

@bp.route('/lecture', methods=['GET'])
def get_lecture():
    args = request.args
    department = args.get('department')
    grade = args.get('grade')
    professor = args.get('professor')
    title = args.get('title')
    lecture_id = args.get('lecture_id')
    response = service.get_lecture(department, grade, professor, title, lecture_id)
    return response
