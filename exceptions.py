class StudentAlreadyExistsError(Exception):
    def __init__(self):
        self.message = 'student already exists in database'
        self.status = 400
        super().__init__(self.message)

class GradeNotQualifiedError(Exception):
    def __init__(self, grade):
        self.message = 'only grade '+grade+' students can attend this lecture'
        self.status = 400
        super().__init__(self.message)

class CreditOverLimitError(Exception):
    def __init__(self):
        self.message = 'student has already taken 9 credits total'
        self.status = 400
        super().__init__(self.message)

class QuotaError(Exception):
    def __init__(self):
        self.message = 'lecture has met students limit'
        self.status = 400
        super().__init__(self.message)

class LectureNotFoundError(Exception):
    def __init__(self, lecture_id):
        self.message = 'cannot find lecture '+lecture_id
        self.status = 400
        super().__init__(self.message)

class RequestTimeError(Exception):
    def __init__(self, start_time, end_time):
        self.message = 'lecture reservation is only available between '+start_time+' ~ '+end_time
        self.status = 400
        super().__init__(self.message)

class VerificationError(Exception):
    def __init__(self, role):
        self.message = role+' must sign in'
        self.status = 401
        super().__init__(self.message)

class AttendanceOverlapError(Exception):
    def __init__(self):
        self.message = 'you already attend this lecture' 
        self.status = 400
        super().__init__(self.message)

class AttendanceNotFoundError(Exception):
    def __init__(self):
        self.message = 'cannot find attendance data'
        self.status = 400
        super().__init__(self.message)

