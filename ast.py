class Node:
    pass


class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class UnaryExpression(Node):
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


class Function(Node):
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return "{}({})".format(self.name, self.argument)


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class If(Node):
    def __init__(self, condition, expression, else_expression=None):
        self.condition = condition
        self.expression = expression
        self.else_expression = else_expression

    def __repr__(self):
        representation = 'IF {} THEN {}'.format(self.condition, self.expression)
        result = representation + ' ELSE {}'.format(self.else_expression) \
            if self.else_expression else representation
        return result


class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class Range(Node):
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return '{}:{}:{}'.format(self.start, self.end, self.step)


class For(Node):
    def __init__(self, id, range, body):
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class Break(Node):
    def __repr__(self):
        return 'BREAK'


class Continue(Node):
    def __repr__(self):
        return 'CONTINUE'


class Return(Node):
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print(Node):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return 'PRINT( {} )'.format(self.expression)


class Access(Node):
    def __init__(self, variable, key):
        self.variable = variable
        self.key = key

    def __repr__(self):
        return '{}[{}]'.format(self.variable, self.key)


class Error(Node):
    pass


class Program(Node):
    def __init__(self, instruction):
        self.instructions = [instruction]


class Start(Node):
    def __init__(self, program):
        self.program = program


class Instruction(Node):
    def __init__(self, line):
        self.line = line


class MatrixInitializer(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Value(Node):
    def __init__(self, primitive):
        self.primitive = primitive

    def __repr__(self):
        return "{}({})".format(type(self.primitive).__name__, self.primitive)


class Rows(Node):
    def __init__(self, sequence):
        self.row_list = [sequence]

    def __repr__(self):
        return "[" + ", ".join(map(str, self.row_list)) + "]"


class Sequence(Node):
    def __init__(self, expression):
        self.expressions = [expression]

    def __repr__(self):
        return "{}".format(self.expressions)
