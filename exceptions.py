class StudentAlreadyExistsError(Exception):
    def __init__(self):
        self.message = 'student already exists in database'
        self.status = 400
        super().__init__(self.message)
