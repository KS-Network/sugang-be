from flask import Blueprint, request, make_response
from typing import Optional
import service
import model
import json
import exceptions

bp = Blueprint('main', __name__, url_prefix='')

def response_200(response, data):
    response.data = json.dumps(data)
    response.status = 200
    return response

def response_error(response, e):
    print(e)
    response.data = json.dumps({ 'error': { e.__class__.__name__: e.message } })
    response.status = e.status
    return response

@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'

@bp.route('/exception', methods=['GET'])
def exception():
    response = make_response()
    e = exceptions.StudentAlreadyExistsError()
    return response_error(response, e)

@bp.route('/sign-in', methods=['POST'])
def sign_in():
    response = make_response()
    student = model.Student(**request.get_json())
    try:
        data = service.sign_in(student)
        if data['success'] == True:
            response.set_cookie('accessToken', data['accessToken'], max_age=60*60*2)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e) 

@bp.route('/sign-up', methods=['POST'])
def sign_up():
    response = make_response()
    student = model.Student(**request.get_json())
    try:
        data = service.sign_up(student)
        if data['success'] == True:
            response.set_cookie('accessToken', data['accessToken'], max_age=60*60*2)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e) 

@bp.route('/lecture', methods=['GET'])
def get_lecture():
    response = make_response()
    args = request.args
    department = args.get('department')
    grade = args.get('grade')
    professor = args.get('professor')
    title = args.get('title')
    lecture_id = args.get('lecture_id')
    try:
        data = service.get_lecture(department, grade, professor, title, lecture_id)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

@bp.route('/student-lecture', methods=['GET'])
def get_student_lecture():
    response = make_response()
    args = request.args
    student_id = args.get('student_id')
    try:
        data = service.get_student_lecture(student_id)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

@bp.route('/attendance', methods=['POST'])
def post_attendance():
    response = make_response()
    attendance = model.Attendance(**request.get_json())
    try:
        data = service.post_attendance(attendance)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

