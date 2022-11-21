import model
import json
from flask import make_response

def verify():
    return model.verify()

def sign_in(student: model.Student):
    data = model.sign_in(student)
    return data

def sign_up(student: model.Student):
    data = model.sign_up(student)
    return data

def get_lecture(department, grade, professor, title, lecture_id):
    data = model.get_lecture(department, grade, professor, title, lecture_id)
    return data
