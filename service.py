import model
import json
from flask import make_response

def verify():
    return model.verify()

def sign_in(student: model.Student):
    response = model.sign_in(student)
    response.status = 200
    return response

def sign_up(student):
    response = None
    try:
        student = model.Student(**student)
        response = model.sign_up(student)
        response.status = 200
    except Exception as e:
        data = {
            'success': False,
            'error': str(e)
        }
        response = make_response(json.dumps(data), 200)
    return response
