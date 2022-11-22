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

def get_lecture(department: str, grade: str, professor: str, title: str, lecture_id: str):
    data = model.get_lecture(department, grade, professor, title, lecture_id)
    return data

def get_student_lecture(student_id):
    data = model.get_student_lecture(student_id)
    return data

def post_attendance(attendance: model.Attendance):
    data = model.post_attendance(attendance)
    return data

