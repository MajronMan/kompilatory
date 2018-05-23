import ast
from matrix_lexer import MatrixLexer
from errors import *
from ast import *


class NodeVisitor:
    def __init__(self):
        self.namespace = dict()
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
        if node.operator == MatrixLexer.t_ASSIGN:
            self.namespace[node.left.name] = node.right
        else:
            self.visit(node.right)

    def visit_BinaryExpression(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_Function(self, node):
        self.visit(node.argument)

    def visit_Variable(self, node):
        if node.name not in self.namespace:
            self.errors.append(InvalidNameError(node.name, node.position))

    def visit_Value(self, node):
        pass

    def visit_UnaryExpression(self, node):
        if type(node.operand) is Variable and node.operand.name not in self.namespace:
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
        if self.loop == 0:
            self.errors.append(StatementNotAllowetOutsideLoopError("return", node.position))

    def visit_Print(self, node):
        self.visit_Sequence(node.expression)

    def visit_Sequence(self, node):
        for expression in node.expressions:
            self.visit(expression)

    def visit_Range(self, node):
        if type(node.start) is int and type(node.end) is int and node.start.primitive > node.end.primitive:
            self.errors.append(InvalidRangeError(node.position))

    def visit_If(self, node):
        self.loop += 1
        self.visit_Expression(node.condition)
        self.visit_Instruction(node.expression)
        if node.else_expression is not None:
            self.visit_Instruction(node.else_expression)
        self.loop -= 1

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
