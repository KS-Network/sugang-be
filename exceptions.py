#this file includes user-defined exceptions
#these exceptions are used to handle 수강신청 예외

#테스트용 예외
class StudentAlreadyExistsError(Exception):
    def __init__(self):
        self.message = 'student already exists in database'
        self.status = 400
        super().__init__(self.message)

#강의의 요구 학년과 신청 학생의 학년이 맞지 않음
class GradeNotQualifiedError(Exception):
    def __init__(self, grade):
        self.message = 'only grade '+grade+' students can attend this lecture'
        self.status = 400
        super().__init__(self.message)

#신청 학점이 9점 이상일 때 신청함
class CreditOverLimitError(Exception):
    def __init__(self):
        self.message = 'student has already taken 9 credits total'
        self.status = 400
        super().__init__(self.message)

#수강 정원이 가득참
class QuotaError(Exception):
    def __init__(self):
        self.message = 'lecture has met students limit'
        self.status = 400
        super().__init__(self.message)

#해당하는 강의를 찾을 수 없음
class LectureNotFoundError(Exception):
    def __init__(self, lecture_id):
        self.message = 'cannot find lecture '+lecture_id
        self.status = 400
        super().__init__(self.message)

#수강 신청 가능 시간이 아님
class RequestTimeError(Exception):
    def __init__(self, start_time, end_time):
        self.message = 'lecture reservation is only available between '+start_time+' ~ '+end_time
        self.status = 400
        super().__init__(self.message)

#로그인 필요
class VerificationError(Exception):
    def __init__(self, role):
        self.message = role+' must sign in'
        self.status = 401
        super().__init__(self.message)

#이미 수강신청한 강의를 수강신청하려고함
class AttendanceOverlapError(Exception):
    def __init__(self):
        self.message = 'you already attend this lecture' 
        self.status = 400
        super().__init__(self.message)

#수강신청 정보를 찾을 수 없음
class AttendanceNotFoundError(Exception):
    def __init__(self):
        self.message = 'cannot find attendance data'
        self.status = 400
        super().__init__(self.message)

