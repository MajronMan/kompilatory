class Node:
    def __init__(self, position):
        self.position = position


class BinaryExpression(Node):
    def __init__(self, left, operator, right, position):
        super().__init__(position)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class UnaryExpression(Node):
    def __init__(self, operator, operand, position, left=True):
        super().__init__(position)
        self.operator = operator
        self.operand = operand
        self.left = left

    def __repr__(self):
        order = [self.operator, self.operand] if self.left else [self.operand, self.operator]
        return '{}{}'.format(*order)


class Negation(UnaryExpression):
    def __init__(self, operand, position):
        super().__init__('-', operand, position)


class Transposition(UnaryExpression):
    def __init__(self, operand, position):
        super().__init__('\'', operand, position, False)


class Assignment(BinaryExpression):
    pass


class Function(Node):
    def __init__(self, name, argument, position):
        super().__init__(position)
        self.name = name
        self.argument = argument

    def __repr__(self):
        return "{}({})".format(self.name, self.argument)


class Variable(Node):
    def __init__(self, name, position):
        super().__init__(position)
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class If(Node):
    def __init__(self, condition, expression, position, else_expression=None):
        super().__init__(position)
        self.condition = condition
        self.expression = expression
        self.else_expression = else_expression

    def __repr__(self):
        representation = 'IF {} THEN {}'.format(self.condition, self.expression)
        result = representation + ' ELSE {}'.format(self.else_expression) \
            if self.else_expression else representation
        return result


class While(Node):
    def __init__(self, condition, body, position):
        super().__init__(position)
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class Range(Node):
    def __init__(self, start, end, position, step=1):
        super().__init__(position)
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return '{}:{}:{}'.format(self.start, self.end, self.step)


class For(Node):
    def __init__(self, id, range, body, position):
        super().__init__(position)
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
    def __init__(self, result, position):
        super().__init__(position)
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print(Node):
    def __init__(self, expression, position):
        super().__init__(position)
        self.expression = expression

    def __repr__(self):
        return 'PRINT( {} )'.format(self.expression)


class Access(Node):
    def __init__(self, variable, key, position):
        super().__init__(position)
        self.variable = variable
        self.key = key

    def __repr__(self):
        return '{}[{}]'.format(self.variable, self.key)


class Error(Node):
    pass


class Program(Node):
    def __init__(self, instruction, position):
        super().__init__(position)
        self.instructions = [instruction]

    def __repr__(self):
        return "\n".join(map(str, self.instructions))


class Start(Node):
    def __init__(self, program):
        super().__init__((0, 0))
        self.program = program

    def __repr__(self):
        return str(self.program)


class Instruction(Node):
    def __init__(self, line, position):
        super().__init__(position)
        self.line = line

    def __repr__(self):
        return str(self.line)


class MatrixInitializer(Node):
    def __init__(self, value, position):
        super().__init__(position)
        self.value = value

    def __repr__(self):
        return str(self.value)


class Value(Node):
    def __init__(self, primitive, position):
        super().__init__(position)
        self.primitive = primitive

    def __repr__(self):
        return "{}({})".format(type(self.primitive).__name__, self.primitive)


class Rows(Node):
    def __init__(self, sequence, position):
        super().__init__(position)
        self.row_list = [sequence]

    def __repr__(self):
        return "[" + ", ".join(map(str, self.row_list)) + "]"


class Sequence(Node):
    def __init__(self, expression, position):
        super().__init__(position)
        self.expressions = [expression]

    def __repr__(self):
        return "{}".format(self.expressions)
