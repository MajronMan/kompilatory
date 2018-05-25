import ast
from matrix_lexer import MatrixLexer
from errors import *
from ast import *
import symbol_table


class NodeVisitor:
    def __init__(self):
        self.symtab = symbol_table.SymbolTable()
        self.loop = 0
        self.errors = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):
    def visit_Start(self, node):
        self.visit(node.program)

    def visit_Program(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Instruction(self, node):
        self.visit(node.line)

    def visit_Assignment(self, node):
        self.visit(node.right)
        if node.operator == MatrixLexer.t_ASSIGN:
            self.symtab.define(node.left.name, node.right)
        else:
            if self.symtab.lookup(node.left.name) is None:
                self.errors.append(InvalidNameError(node.left.name, node.position))

    def visit_BinaryExpression(self, node):
        self.visit(node.right)
        self.visit(node.left)

        if type(node.left) is Value and type(node.right) is Value:
            if type(node.left.primitive) is Matrix:
                if not node.left.primitive.dims_compatible(node.right.primitive):
                    self.errors.append(ArithmeticOperationError(
                        node.position, "Matrix dimension or type mismatch"
                    ))
                    return
            elif type(node.right.primitive) is Matrix:
                if not node.right.primitive.dims_compatible(node.left.primitive):
                    self.errors.append(ArithmeticOperationError(
                        node.position, "Matrix dimension or type mismatch"
                    ))

    def visit_Function(self, node):
        def check_value_type(n, errors):
            if type(n) is Value and type(n.primitive) is not int:
                errors.append(
                    ArgumentError(
                        n.position,
                        'Argument must be int or sequence of ints, {} given'.format(type(n.primitive).__name__)
                    )
                )
        self.visit(node.argument)
        check_value_type(node.argument, self.errors)
        if type(node.argument) is Sequence:
            l = len(node.argument.expressions)
            if l == 0 or l > 2:
                self.errors.append(
                    ArgumentError(
                        node.position,
                        'Argument must be int or sequence of length 1 or 2, not {}'.format(l)
                    )
                )
            else:
                for v in node.argument.expressions:
                    check_value_type(v, self.errors)

    def visit_Variable(self, node):
        if self.symtab.lookup(node.name) is None:
            self.errors.append(InvalidNameError(node.name, node.position))

    def visit_Value(self, node):
        if type(node.primitive) is Matrix:
            self.visit_Matrix(node.primitive)
        elif type(node.primitive) is Access:
            self.visit_Access(node.primitive)

    def visit_UnaryExpression(self, node):
        if type(node.operand) is Variable and self.symtab.lookup(node.operand.name) is None:
            self.errors.append(InvalidNameError(node.name, node.position))

    def visit_Transposition(self, node):
        self.visit_UnaryExpression(node)

    def visit_Negation(self, node):
        self.visit_UnaryExpression(node)

    def visit_Expression(self, node):
        if type(node) is BinaryExpression:
            self.visit(node.left)
            self.visit(node.right)

    def visit_Break(self, node):
        if self.loop == 0:
            self.errors.append(StatementNotAllowetOutsideLoopError("break", node.position))

    def visit_Continue(self, node):
        if self.loop == 0:
            self.errors.append(StatementNotAllowetOutsideLoopError("continue", node.position))

    def visit_Return(self, node):
        pass

    def visit_Print(self, node):
        self.visit_Sequence(node.expression)

    def visit_Sequence(self, node):
        for expression in node.expressions:
            self.visit(expression)

    def visit_Range(self, node):
        nodes = [node.start, node.end, node.step]
        values = []
        valid_types = [Value, Variable]
        # for n in nodes:
        #     if type(n) not in valid_types:
        #         self.errors.append(InvalidRangeError(node.position, 'Only integers allowed in range'))
        #         return
        #     if type(n) is Variable:
        #         l = self.symtab.lookup(node.name)
        #         if self.symtab.lookup(node.name) is None:
        #             self.errors.append(InvalidNameError(node.name, node.position))
        #         elif l.stype is not int:
        #             self.errors.append(InvalidRangeError(node.position, 'Only integers allowed in range'))
        #             return
        #     else:
        #
        #         values.append(n)

    def visit_If(self, node):
        self.visit_Expression(node.condition)
        self.visit_Instruction(node.expression)
        if node.else_expression is not None:
            self.visit_Instruction(node.else_expression)

    def visit_While(self, node):
        self.loop += 1
        self.visit_Expression(node.condition)
        self.visit_Instruction(node.body)
        self.loop -= 1

    def visit_For(self, node):
        self.loop += 1
        self.visit(node.range)
        self.visit_Instruction(node.body)
        self.loop -= 1

    def visit_Matrix(self, node):
        if not node.has_correct_dims():
            self.errors.append(MatrixDimensionsError(node.position))

    def visit_Access(self, node):
        val = self.symtab.lookup(node.variable)
        if type(val) is Value and type(val.primitive) is Matrix:
            keys = node.key.expressions
            l = len(keys)
            if l > 2 or l == 0:
                self.errors.append(MatrixAccessError(
                    node.position, 'Access requires one or two values, {} given'.format(l)
                ))
                return
            for (i, k) in enumerate(keys):
                if type(k) is Value:
                    if type(k.primitive) is int and k.primitive >= val.primitive.dims[i]:
                        self.errors.append(MatrixAccessError(
                            node.position, 'index {} out of range'.format(k)
                        ))
                        return
                    elif type(k.primitive) is str or type(k.primitive) is float:
                        self.errors.append(MatrixAccessError(
                            node.position, 'Matrix key must be integer, not {}'.format(type(k.primitive).__name__)
                        ))
                        return
