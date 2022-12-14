import model
import json
from flask import make_response
import exceptions

#이 파일은 각각 API들에 대하여 예외 처리를 담당하는 로직을 포함하고 있다.

def verify():
    return model.verify()

def verify_admin():
    return model.verify_admin();

def sign_in(student: model.Student):
    data = model.sign_in(student)
    return data

def sign_in_admin(admin: model.Admin):
    data = model.sign_in_admin(admin)
    return data

def sign_up(student: model.Student):
    data = model.sign_up(student)
    return data

def get_lecture(department: str, grade: str, professor: str, title: str, lecture_id: str):
    data = model.get_lecture(department, grade, professor, title, lecture_id)
    return data

def put_lecture(lecture: model.Lecture):
    if not verify_admin(): raise exceptions.VerificationError('admin')
    if not model.lecture_exists(lecture.lecture_id): raise exceptions.LectureNotFoundError(lecture.lecture_id)
    data = model.put_lecture(lecture)
    return data

def delete_lecture(lecture_id: str):
    if not verify_admin(): raise exceptions.VerificationError('admin')
    if not model.lecture_exists(lecture_id): raise exceptions.LectureNotFoundError(lecture_id)
    data = model.delete_lecture(lecture_id)
    return data

def get_student_lecture(student_id: str):
    if not verify(): raise exceptions.VerificationError('student')
    data = model.get_student_lecture(student_id)
    return data

def post_attendance(attendance: model.Attendance):
    if not verify(): raise exceptions.VerificationError('student')
    #time = model.get_time()
    #if not model.check_time(): raise exceptions.RequestTimeError(time['start'], time['end'])
    if not model.lecture_exists(attendance.lecture_id): raise exceptions.LectureNotFoundError(attendance.lecture_id)
    if model.student_attendance_exists(attendance.lecture_id, attendance.student_id): raise exceptions.AttendanceOverlapError
    if not model.grade_qualified(attendance.lecture_id, attendance.student_id): raise exceptions.GradeNotQualifiedError(str(model.get_lecture_grade(attendance.lecture_id)))
    if model.get_credit(attendance.student_id)>=9: raise exceptions.CreditOverLimitError
    if model.quota_exceeded(attendance.lecture_id): raise exceptions.QuotaError
    data = model.post_attendance(attendance)
    return data

def delete_attendance(lecture_id: str, student_id: str):
    if not verify(): raise exceptions.VerificationError('student')
    if not model.attendance_exists(lecture_id): raise exceptions.AttendanceNotFoundError
    data = model.delete_attendance(lecture_id, student_id)
    return data

def put_time(time):
    if not verify_admin(): raise exceptions.VerificationError('admin')
    data = model.put_time(time)
    return data

