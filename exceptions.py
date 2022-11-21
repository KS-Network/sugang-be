class StudentAlreadyExistsError(Exception):
    def __init__(self):
        self.message = 'student already exists in database'
        super().__init__(self.message)
