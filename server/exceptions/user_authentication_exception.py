from exceptions.basic_exception import BasicException

class UserAuthenticationException(BasicException):
    def __init__(self):
        super(UserAuthenticationException, self).__init__('User not found.')

