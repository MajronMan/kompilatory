class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class Relation(BinaryExpression):
    pass


class UnaryExpression:
    def __init__(self, operator, operand, left=True):
        self.operator = operator
        self.operand = operand
        self.left = left

    def __repr__(self):
        order = [self.operator, self.operand] if self.left else [self.operand, self.operator]
        return '{}{}'.format(*order)


class Negation(UnaryExpression):
    def __init__(self, operand):
        super().__init__('-', operand)


class Transposition(UnaryExpression):
    def __init__(self, operand):
        super().__init__('\'', operand, False)


class Assignment(BinaryExpression):
    pass


class Function:
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return "{}({})".format(self.name, self.argument)


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class If:
    def __init__(self, condition, expression, else_expression=None):
        self.condition = condition
        self.expression = expression
        self.else_expression = else_expression

    def __repr__(self):
        representation = 'IF {} THEN {}'.format(self.condition, self.expression)
        result = representation + ' ELSE {}'.format(self.else_expression) \
            if self.else_expression else representation
        return result


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class Range:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return '{}:{}:{}'.format(self.start, self.end, self.step)


class For:
    def __init__(self, id, range, body):
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class Break:
    def __repr__(self):
        return 'BREAK'


class Continue:
    def __repr__(self):
        return 'CONTINUE'


class Return:
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return 'PRINT( {} )'.format(self.expression)


class Access:
    def __init__(self, variable, key):
        self.variable = variable
        self.key = key

    def __repr__(self):
        return '{}[{}]'.format(self.variable, self.key)
