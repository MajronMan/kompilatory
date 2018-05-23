class TypeException(Exception):
    reason = ''

    def __init__(self, line_no=None):
        self.line_no = line_no

    def __str__(self):
        return '{} at line {}: '.format(self.__class__.__name__, self.line_no) + self.reason


class InvalidNameError(TypeException):
    def __init__(self, name, line_no=None):
        super().__init__(line_no)
        self.name = name
        self.reason = '{} undefined.'.format(self.name)


class InvalidRangeError(TypeException):
    def __init__(self, line_no=None):
        super().__init__(line_no)
        self.reason = 'Invalid range'.format()


class StatementNotAllowetOutsideLoopError(TypeException):
    def __init__(self, statement_name, line_no=None):
        super().__init__(line_no)
        self.reason = 'Statement {} not allowed outside of loop'.format(statement_name)