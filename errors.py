class TypeException(Exception):
    def __init__(self, position, reason):
        self.position = position
        self.reason = reason

    def __repr__(self):
        return '{}: {} at line {}'.format(self.__class__.__name__, self.reason, self.position)

    __str__ = __repr__


class MatrixDimensionsError(TypeException):
    def __init__(self, position):
        super().__init__(position, 'Matrix needs to have rows of equal length')


class ArithmeticOperationError(TypeException):
    pass


class MatrixAccessError(TypeException):
    pass


class InvalidNameError(TypeException):
    def __init__(self, name, position):
        super().__init__(position, '{} undefined'.format(name))
        self.name = name


class InvalidRangeError(TypeException):
    def __init__(self, position, addition):
        super().__init__(position, 'Invalid range ' + str(addition))


class StatementNotAllowetOutsideLoopError(TypeException):
    def __init__(self, statement_name, position):
        super().__init__(position, 'Statement {} not allowed outside of loop'.format(statement_name))


class ArgumentError(TypeException):
    pass
