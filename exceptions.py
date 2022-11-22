class StudentAlreadyExistsError(Exception):
    def __init__(self):
        self.message = 'student already exists in database'
        super().__init__(self.message)

class GradeNotQualifiedError(Exception):
    def __init__(self, grade):
        self.message = 'only '+grade+' grade student can attend this lecture'
        self.status = 400
        super().__init__(self.message)

class CreditOverLimitError(Exception):
    def __init__(self):
        self.message = 'student has already taken 9 credits total'
        self.status = 400
        super().__init__(self.message)

class LectureNotFoundError(Exception):
    def __init__(self, lecture_id):
        self.message = 'cannot find lecture '+lecture_id
        self.status = 400
        super().__init__(self.message)

class RequestTimeError(Exception):
    def __init__(self):
        self.message = 'lecture reservation is only available between 09:00 ~ 18:00'
        self.status = 400
        super().__init__(self.message)
