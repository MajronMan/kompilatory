class TypeException(Exception):
    reason = ''

    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return '{}: {} at line {}'.format(self.__class__.__name__, self.reason, self.position)


class InvalidNameError(TypeException):
    def __init__(self, name, position):
        super().__init__(position)
        self.name = name
        self.reason = '{} undefined'.format(self.name)


class InvalidRangeError(TypeException):
    def __init__(self, position):
        super().__init__(position)
        self.reason = 'Invalid range'.format()


class StatementNotAllowetOutsideLoopError(TypeException):
    def __init__(self, statement_name, position):
        super().__init__(position)
        self.reason = 'Statement {} not allowed outside of loop'.format(statement_name)
