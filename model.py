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

class Lecture(BaseModel):
    department: str
    grade: int
    credit: int
    title: str
    lecture_id: str
    professor: str
    quota: int
    attendance: str

class Attendance(BaseModel):
    lecture_id: str
    student_id: str

class Admin(BaseModel):
    email: str
    password: str

def get_attendance(lecture_id: str):
    c.execute(
        'select count(*) from attendance where lecture_id=%s;',
        (lecture_id, )
    )
    result = c.fetchall()
    return int(result[0][0])

def verify():
    encoded = request.cookies.get('studentToken')
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
        data['studentToken'] = encoded
    return data

def sign_up(student: Student):
    data = { 'error': None, 'success': False }
    m = hashlib.sha256()
    m.update(student.password.encode('utf-8'))
    student.password = m.hexdigest()
    try:
        c.execute(
            'insert into student values (%s, %s, %s, %s, %s);',
            (student.email, student.student_id, student.password, student.name, student.grade)
        )
        conn.commit()
        encoded = jwt.encode({'student_id': student.student_id}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        data['success'] = True
        data['studentToken'] = encoded
    except Exception as e:
        conn.commit()
    return data

def get_lecture(department: str, grade: str, professor: str, title: str, lecture_id: str):
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
                attendance=get_attendance(temp[4])
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
    c.execute(
        '''select department, grade, credit, title, l.lecture_id, professor, quota
        from attendance a
        left outer join lecture l on a.lecture_id=l.lecture_id
        where student_id=%s;''',
        (student_id, )
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
                attendance=get_attendance(temp[4])
            )
            arr.append(lecture.dict())
        data['data'] = arr
    return data

def post_attendance(attendance: Attendance):
    data = {'error': None, 'success': False}
    try:
        c.execute(
            'insert into attendance values (%s, %s)',
            (attendance.lecture_id, attendance.student_id)
        )
        conn.commit()
        data['success'] = True
    except Exception as e:
        conn.commit()
    return data

def delete_attendance(lecture_id: str, student_id: str):
    data = {'error': None, 'success': False}
    try:
        c.execute(
            'delete from attendance where lecture_id=%s and student_id=%s',
            (lecture_id, student_id)
        )
        conn.commit()
        data['success'] = True
    except Exception as e:
        conn.commit()
    return data

