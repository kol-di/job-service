class UnknownUserType(Exception):
    def __init__(self, user_type):
        self.user_type = user_type
        self.message = f'Unknown user type {self.user_type}'
        super().__init__(self.message)
