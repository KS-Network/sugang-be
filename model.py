import psycopg2
import json
from typing import Optional, List
from pydantic import BaseModel
from flask import make_response, request
import jwt, hashlib

conn = psycopg2.connect(host="localhost", dbname="ks-network", user="blue", password="toor", port="5432")
c = conn.cursor()

class Student(BaseModel):
    email: Optional[str]
    student_id: str
    password: str
    name: Optional[str]
    grade: Optional[int]
    credit: Optional[int]

class Lecture(BaseModel):
    department: str
    grade: int
    credit: int
    title: str
    lecture_id: str
    class_no: str
    professor: str
    quota: int
    attendance: int

class Attendance(BaseModel):
    leture_id: str
    class_no: str
    student_id: str

class Admin(BaseModel):
    email: str
    password: str

def verify():
    encoded = request.cookies.get('accessToken')
    if not encoded: return False
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    result = c.execute(
        'select * from student where student_id=%s;',
        (decoded['student_id'])
    )
    return result

def sign_in(student: Student):
    response = make_response()
    data = { 'success': False }
    m = hashlib.sha256()
    m.update(student.password.encode('utf-8'))
    student.password = m.hexdigest()
    try:
        c.execute(
            'select student_id from student where student_id=%s and password=%s;',
            (student.student_id, student.password)
        )
        result = c.fetchall()
        if result:
            student_id = result[0][0]
            encoded = jwt.encode({'student_id': student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
            response.set_cookie('accessToken', encoded, max_age=60*60*2)
            data['success'] = True
    except Exception as e:
        data['error'] = str(e)
    response.data = json.dumps(data)
    return response

def sign_up(student: Student):
    response = make_response()
    data = { 'success': False }
    m = hashlib.sha256()
    m.update(student.password.encode('utf-8'))
    student.password = m.hexdigest()
    try:
        c.execute(
            'insert into student values (%s, %s, %s, %s, %s, %s);',
            (student.email, student.student_id, student.password, student.name, student.grade, student.credit)
        )
        conn.commit()
        encoded = jwt.encode({'student_id': student.student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        response.set_cookie('accessToken', encoded, max_age=60*60*2)
        data['success'] = True
    except Exception as e:
        data['error'] = str(e)
        conn.commit()
    response.data = json.dumps(data)
    return response
