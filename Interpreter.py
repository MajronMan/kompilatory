import operator
import numpy as np
import ast
from Memory import *
from Exceptions import *
from visit import *
import sys

bin_ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    ".+": operator.add,
    ".-": operator.sub,
    ".*": np.multiply,
    "./": np.divide,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}
un_ops = {
    "NEGATION": operator.neg,
    "TRANSPOSE": np.transpose
}

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(ast.Node)  # DONE
    def visit(self, node):
        pass

    @when(ast.Start)  # Done
    def visit(self, node):
        return self.visit(node.program)

    @when(ast.Program)  # DONE
    def visit(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(ast.Instruction)  # Done
    def visit(self, node):
        return self.visit(node.line)

    @when(ast.BinaryExpression)  # Done
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return bin_ops[node.operator](r1, r2)

    @when(ast.UnaryExpression)  # Done
    def visit(self, node):
        r1 = node.operand.accept()
        return un_ops[node.operator](r1)

    @when(ast.Function)
    def visit(self, node):
        if node.name == "zeros":
            return np.zeros(node.argument.primitive)
        else:
            if node.name == "eye":
                return np.eye(node.argument.primitive)
            else:
                if node.name == "ones":
                    return np.ones(node.argument.primitive)

    @when(ast.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(ast.If)  # DONE
    def visit(self, node):
        if node.condition.accept(self):
            return node.expression.accept(self)
        else:
            if node.else_expression:
                return node.else_expression.accept(self)

    @when(ast.While)  # DONE
    def visit(self, node):
        r = None
        while node.condition.accept(self):
            r = node.body.accept(self)
        return r

    @when(ast.Range)  # Done
    def visit(self, node):

        start = node.start.accept(self);
        end = node.end.accept(self);

        if type(start) == str:
            start = self.memory_stack.get(start)
        if type(end) == str:
            end = self.memory_stack.get(end)

        return range(start, end)

    @when(ast.For)
    def visit(self, node):
        r = None
        for i in node.range.accept(self):
            self.memory_stack.insert(node.id, i)
            r = node.body.accept(self)
        return r

    @when(ast.Break)  # DONE
    def visit(self, node):
        raise BreakException()

    @when(ast.Continue)  # DONE
    def visit(self, node):
        raise ContinueException()

    @when(ast.Return)  # DONE
    def visit(self, node):
        raise ReturnValueException(node.result.accpet(self))

    @when(ast.Print)
    def visit(self, node):
        for i in node.expression:
            print(i.accept(self))

    @when(ast.Access)
    def visit(self, node):

        matrix = self.memory_stack.get(node.variable)

        for x in node.key:
            matrix = matrix[x.accept(self)]
        return matrix.accept(self)

    @when(ast.Error)
    def visit(self, node):
        pass

    @when(ast.Matrix)
    def visit(self, node):
        return np.array(node.rows.accept(self))

    @when(ast.Rows)
    def visit(self, node):
        return node.row_list

    @when(ast.Sequence)
    def visit(self, node):
        val = 0
        for x in node.expressions:
            val = val + x.accept(self)
            print(x.accept(self))
        return val

    @when(ast.Value)  # done
    def visit(self, node):
        if type(node.primitive) == int or type(node.primitive) == str:
            return node.primitive
        else:
            return node.primitive.accept(self);

    @when(ast.Assignment)
    def visit(self, node):
        right=None;
        left=None;
        if node.operator == "=":
            right = node.right.accept(self)
            left = node.left.name
        elif node.operator == "+=":
            right = node.right.accept(self)
            right = operator.add(right, node.left.accept(self))
            left = node.left.name
        elif node.operator == "*=":
            right = node.right.accept(self)
            right = operator.mul(right, node.left.accept(self))
            left = node.left.name
        elif node.operator == "/=":
            right = node.right.accept(self)
            right = operator.truediv(right, node.left.accept(self))
            left = node.left.name
        elif node.operator == "-=":
            right = node.right.accept(self)
            right = operator.sub(right, node.left.accept(self))
            left = node.left.name

        if type(left) == ast.Access:
            matrix = self.memory_stack.get(left.variable)
            matrix[left.key[0].accept(self)][left.key[1].accept(self)] = right
            self.memory_stack.insert(left.variable, matrix)
        else:
            self.memory_stack.insert(left, right)

    @when(ast.Transposition)
    def visit(self, node):
        r1 = node.operand.accept(self)
        return np.transpose(r1)

    @when(ast.Negation)
    def visit(self, node):
        r1 = node.operand.accept(self)
        return operator.neg(r1)
