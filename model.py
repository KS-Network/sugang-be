import os
import psycopg2
import json
from typing import Optional, List
from pydantic import BaseModel
from flask import make_response, request
import jwt, hashlib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

conn = psycopg2.connect( #데이터베이스 연결
    host=os.environ['host'],
    dbname=os.environ['dbname'],
    user=os.environ['user'],
    password=os.environ['password'],
    port=os.environ['port']
)
c = conn.cursor() #데이터베이스 연결

#이 클래스들은 타이핑 및 데이터베이스에 정의된 모델을 활용하기 위함
class Student(BaseModel): # 학생 클래스
    email: Optional[str]
    student_id: str
    password: str
    name: Optional[str]
    grade: Optional[int]

class Lecture(BaseModel): #강의 클래스
    department: str
    grade: int
    credit: int
    title: str
    lecture_id: str
    professor: str
    quota: int
    attendance: Optional[str]

class Attendance(BaseModel): #수강신청 클래스
    lecture_id: str
    student_id: str

class Admin(BaseModel): #관리자 클래스
    email: str
    password: str

#해당하는 강의가 존재하는지 확인하는 함수
def lecture_exists(lecture_id: str):
    try:
        c.execute(
            'select lecture_id from lecture where lecture_id=%s',
            (lecture_id, )
        )
        result = c.fetchall()
        return result
    except Exception as e:
        return False

#해당하는 수강신청 내역이 존재하는지 확인하는 함수
def attendance_exists(lecture_id: str):
    try:
        c.execute(
            'select lecture_id from attendance where lecture_id=%s',
            (lecture_id, )
        )
        result = c.fetchall()
        return result
    except Exception as e:
        return False

#학생이 해당 강의에 대해서 이미 수강신청을 했는지 확인하는 함수
def student_attendance_exists(lecture_id: str, student_id: str):
    try:
        c.execute(
            'select lecture_id from attendance where lecture_id=%s and student_id=%s',
            (lecture_id, student_id)
        )
        result = c.fetchall()
        return result
    except Exception as e:
        return False

#현재 수강신청 가능한 시간인지 확인하는 함수
def check_time():
    try:
        cur_time = int(datetime.now().strftime('%H%M'))
        with open('time.json', 'r') as file:
            time = json.load(file)
        if time: 
            start_time = int(time['start'])
            end_time = int(time['end'])
            return start_time <= cur_time <= end_time
    except Exception as e:
        return False

#강의의 수강 가능 학년을 가져오는 함수
def get_lecture_grade(lecture_id: str):
    try:
        c.execute(
            'select grade from lecture where lecture_id=%s',
            (lecture_id, )
        )
        result = c.fetchall()
        return result[0][0]
    except Exception as e:
        return None

#학생의 학년을 가져오는 함수
def get_student_grade(student_id: str):
    try:
        c.execute(
            'select grade from student where student_id=%s',
            (student_id, )
        )
        result = c.fetchall()
        return result[0][0]
    except Exception as e:
        return None

#학생이 신청하고자 하는 강의의 요구 학년에 부합하는지 확인하는 함수
def grade_qualified(lecture_id: str, student_id: str):
    lecture_grade = get_lecture_grade(lecture_id)
    student_grade = get_student_grade(student_id)
    return lecture_grade == student_grade

#학생의 현재 신청 학점을 계산하는 함수
def get_credit(student_id: str):
    try:
        c.execute(
            'select sum(l.credit) from attendance a left outer join lecture l on a.lecture_id=l.lecture_id where a.student_id=%s',
            (student_id, )
        )
        result = c.fetchall()
        return result[0][0] if result[0][0] else 0
    except Exception as e:
        return 0

#강의의 수강신청 정원을 가져오는 함수
def get_quota(lecture_id: str):
    try:
        c.execute(
            'select quota from lecture where lecture_id=%s',
            (lecture_id, )
        )
        result = c.fetchall()
        return result[0][0]
    except Exception as e:
        return 0

#강의의 현재 수강신청 인원을 가져오는 함수
def get_attendance(lecture_id: str):
    try:
        c.execute(
            'select count(*) from attendance where lecture_id=%s;',
            (lecture_id, )
        )
        result = c.fetchall()
        return result[0][0] if result[0][0] else 0
    except Exception as e:
        return 0

#강의의 수강신청 정원이 꽉 찼는지 확인하는 함수
def quota_exceeded(lecture_id: str):
    quota = get_quota(lecture_id)
    attendance = get_attendance(lecture_id)
    return quota <= attendance

#현재 수강 신청 가능 시간을 가져오는 함수
def get_time():
    try:
        with open('time.json', 'r') as file:
            time = json.load(file)
            return time
    except Exception as e:
        return {}

#수강신청 가능 시간을 변경하는 함수
def put_time(time):
    data = {'error': None, 'success': False}
    try:
        with open('time.json', 'w') as file:
            file.write(json.dumps(time))
        data['success'] = True
    except Exception as e:
        print(e)
        pass
    return data

#로그인 여부를 확인하는 함수
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

def verify_admin():
    encoded = request.cookies.get('adminToken')
    if not encoded: return False
    decoded = jwt.decode(encoded, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithms=["HS256"])
    try:
        c.execute(
            'select * from admin where email=%s;',
            (decoded['email'], )
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

def sign_in_admin(admin: Admin):
    data = { 'error': None, 'success': False }
    m = hashlib.sha256()
    m.update(admin.password.encode('utf-8'))
    admin.password = m.hexdigest()
    c.execute(
        'select email from admin where email=%s and password=%s;',
        (admin.email, admin.password)
    )
    result = c.fetchall()
    if result:
        email = result[0][0]
        encoded = jwt.encode({'email': email}, 'JEfWefI0E1qlnIz06qmob7cZp5IzH/i7KwOI2xqWfhE=', algorithm='HS256')
        data['success'] = True
        data['adminToken'] = encoded
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

def put_lecture(lecture: Lecture):
    data = {'error': None, 'success': False}
    try:
        c.execute(
            '''update lecture set
            department=%s, grade=%s, credit=%s, title=%s, lecture_id=%s, professor=%s, quota=%s
            where lecture_id=%s;''',
            (lecture.department, lecture.grade, lecture.credit, lecture.title, lecture.lecture_id, lecture.professor, lecture.quota, lecture.lecture_id)
        )
        conn.commit()
        data['success'] = True
    except Exception as e:
        conn.commit()
    return data

def delete_lecture(lecture_id: str):
    data = {'error': None, 'success': False}
    try:
        c.execute(
            '''select s.student_id, s.email 
            from attendance a left outer join student s on a.student_id=s.student_id
            where a.lecture_id=%s''',
            (lecture_id, )
        )
        result = c.fetchall()
        if result:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            #smtp.connect("smtp.gmail.com",587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('oponeuser7@gmail.com', 'viybvtoplvjuxjhr')
            msg = MIMEText('안녕하세요. 충남대학교입니다.\n학생께서 수강신청하신 '+lecture_id+' 번 과목이 폐강되었음을 알립니다.')
            msg['Subject'] = '[충남대학교]폐강 알림'
            for student in result:
                email = student[1]
                smtp.sendmail('oponeuser7@gmail.com', email, msg.as_string())
            smtp.quit()
        c.execute(
            'delete from lecture where lecture_id=%s',
            (lecture_id, )
        )
        conn.commit()
        data['success'] = True
    except Exception as e:
        print(e)
        conn.commit()
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

