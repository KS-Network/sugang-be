from flask import Blueprint, request, make_response
from typing import Optional
import service
import model
import json
import exceptions

#controller mamages API endpoints and makes responses

bp = Blueprint('main', __name__, url_prefix='/api')

#200 status response maker
def response_200(response, data):
    response.data = json.dumps(data)
    response.status = 200
    return response

#error response maker
def response_error(response, e):
    print(e)
    response.data = json.dumps({ 'error': { e.__class__.__name__: e.message } })
    response.status = e.status
    return response

#test function
@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'

#test function
@bp.route('/exception', methods=['GET'])
def exception():
    response = make_response()
    e = exceptions.StudentAlreadyExistsError()
    return response_error(response, e)

#sign in and set cookie
@bp.route('/sign-in', methods=['POST'])
def sign_in():
    response = make_response()
    student = model.Student(**request.get_json())
    try:
        data = service.sign_in(student)
        if data['success'] == True:
            response.set_cookie('studentToken', data['studentToken'], max_age=60*60*2)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e) 

#sign in function for adminstrator
@bp.route('/sign-in-admin', methods=['POST'])
def sign_in_admin():
    response = make_response()
    admin = model.Admin(**request.get_json())
    try:
        data = service.sign_in_admin(admin)
        if data['success'] == True:
            response.set_cookie('adminToken', data['adminToken'], max_age=60*60*2)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

#sign-up function (not used)
@bp.route('/sign-up', methods=['POST'])
def sign_up():
    response = make_response()
    student = model.Student(**request.get_json())
    try:
        data = service.sign_up(student)
        if data['success'] == True:
            response.set_cookie('studentToken', data['accessToken'], max_age=60*60*2)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e) 

#get all lecture or find lecture recording to parameters
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

#updates lecture info
@bp.route('/lecture', methods=['PUT'])
def put_lecture():
    response = make_response()
    lecture = model.Lecture(**request.get_json())
    try:
        data = service.put_lecture(lecture)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

#deletes lecture and email notification
@bp.route('/lecture', methods=['DELETE'])
def delete_lecture():
    response = make_response()
    args = request.args
    lecture_id = args.get('lecture_id')
    try:
        data = service.delete_lecture(lecture_id)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

#get lecture which student attends
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

#수강신청 함수
@bp.route('/attendance', methods=['POST'])
def post_attendance():
    response = make_response()
    attendance = model.Attendance(**request.get_json())
    try:
        data = service.post_attendance(attendance)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

#수강 취소 함수
@bp.route('/attendance', methods=['DELETE'])
def delete_attendance():
    response = make_response()
    args = request.args
    lecture_id = args.get('lecture_id')
    student_id = args.get('student_id')
    try:
        data = service.delete_attendance(lecture_id, student_id)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

# 수강신청 가능 시간 변경 함수
@bp.route('/time', methods=['PUT'])
def put_time():
    response = make_response()
    time = request.get_json()
    try:
        data = service.put_time(time)
        return response_200(response, data)
    except Exception as e:
        return response_error(response, e)

