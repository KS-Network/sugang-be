import os
import psycopg2
import json
from typing import Optional, List
from pydantic import BaseModel
from flask import make_response, request
import jwt, hashlib

conn = psycopg2.connect(
    host=os.environ['host'],
    dbname=os.environ['dbname'],
    user=os.environ['user'],
    password=os.environ['password'],
    port=os.environ['port']
)
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
    try:
        c.execute(
            'select * from student where student_id=%s;',
            (decoded['student_id'], )
        )
        result = c.fetchall()
        return result
    except Exception as e:
        return False

def sign_in(student: Student):
    data = { 'error': None, 'success': False }
    m = hashlib.sha256()
    m.update(student.password.encode('utf-8'))
    student.password = m.hexdigest()
    c.execute(
        'select student_id from student where student_id=%s and password=%s;',
        (student.student_id, student.password)
    )
    result = c.fetchall()
    if result:
        student_id = result[0][0]
        encoded = jwt.encode({'student_id': student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        data['success'] = True
        data['accessToken'] = encoded
    return data

def sign_up(student: Student):
    data = { 'error': None, 'success': False }
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
        data['success'] = True
        data['accessToken'] = encoded
    except Exception as e:
        conn.commit()
    return data

def get_lecture(department: str, grade: int, professor: str, title: str, lecture_id: str):
    data = {'error': None, 'data': []}
    c.execute(
        'select * from lecture;'
    )
    result = c.fetchall()
    if result:
        arr = []
        for temp in result:
            lecture = Lecture(
                department=temp[0],
                grade=temp[1],
                credit=temp[2],
                title=temp[3],
                lecture_id=temp[4],
                professor=temp[5],
                quota=temp[6],
                attendance=temp[7]
            )
            cond_department = department==lecture.department if department else True
            cond_grade = grade==lecture.grade if grade else True
            cond_professor = professor==lecture.professor if professor else True
            cond_title = title in lecture.title if title else True
            cond_lecture_id = lecture_id==lecture.lecture_id if lecture_id else True
            if cond_department and cond_grade and cond_professor and cond_title and cond_lecture_id: arr.append(lecture.dict())
        data['data'] = arr
    return data

def get_student_lecture(student_id: str):
    data = {'error': None, 'data': []}
    return data

def post_attendance(attendance: Attendance):
    data = {'error': None, 'success': False}
    try:
        c.execute(
            'insert into attendance values (%s, %s, %s)',
            (attendance.lecture_id, attendance.class_no, attendance.student_id)
        )
        conn.commit()
        data['success'] = True
    except Exception as e:
        conn.commit()
    return data

