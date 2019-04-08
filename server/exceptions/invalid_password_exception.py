from exceptions.basic_exception import BasicException

class InvalidPasswordException(BasicException):
    def __init__(self):
        super(InvalidPasswordException, self).__init__('The password is invalid.')

