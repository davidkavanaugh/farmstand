
class PasswordMatch(Exception):
    def __init__(self, error, message):
        super().__init__(message)
        self.error = error
        # Display the errors
        print(f'ERROR: {error}, MESSAGE: {message}')


class PasswordFormat(Exception):
    def __init__(self, error, message):
        super().__init__(message)
        self.error = error
        # Display the errors
        print(f'ERROR: {error}, MESSAGE: {message}')


class UserExists(Exception):
    def __init__(self, error, message):
        super().__init__(message)
        self.error = error
        # Display the errors
        print(f'ERROR: {error}, MESSAGE: {message}')


class OtherSignUpError(Exception):
    def __init__(self, error):
        self.error = error
        # Display the errors
        print(f'ERROR: {error}')
