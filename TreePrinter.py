import ast

separator = '|   '


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(ast.Node)
    def printTree(self, indent=0):
        res = separator * indent
        res += self.printTree(indent)
        return res

    @addToClass(ast.BinaryExpression)
    def printTree(self, indent=0):
        res = indent * separator + str(self.operator) + '\n'
        res += self.left.printTree(indent + 1)
        res += self.right.printTree(indent + 1)
        return res

    @addToClass(ast.UnaryExpression)
    def printTree(self, indent=0):
        res = ""
        res += indent * separator + str(self.operator) + '\n'
        res += self.operand.printTree(indent + 1)
        return res

    @addToClass(ast.Function)
    def printTree(self, indent=0):
        res = indent * separator + str(self.name) + '\n'
        res += self.argument.printTree(indent + 1)
        return res

    @addToClass(ast.Variable)
    def printTree(self, indent=0):
        return indent * separator + str(self.name) + '\n'

    @addToClass(ast.If)
    def printTree(self, indent=0):
        res = indent * separator + "IF\n"
        res += self.condition.printTree(indent + 1)
        res += indent * separator + "THEN\n"
        res += self.expression.printTree(indent + 1)
        if self.else_expression is not None:
            res += indent * separator + "ELSE\n"
            res += self.else_expression.printTree(indent + 1)
        return res

    @addToClass(ast.While)
    def printTree(self, indent=0):
        res = indent * separator + "WHILE\n"
        res += self.condition.printTree(indent + 1)
        res += self.body.printTree(indent + 1)
        return res

    @addToClass(ast.Range)
    def printTree(self, indent=0):
        res = indent * separator + "["
        res += str(self.start) + ":"
        res += str(self.end) + ":"
        res += str(self.step) + "]\n"
        return res

    @addToClass(ast.For)
    def printTree(self, indent=0):
        res = ""
        res += indent * separator + "FOR" + "\n"
        res += (indent + 1) * separator + str(self.id) + "\n"
        res += self.range.printTree(indent + 1)
        res += self.body.printTree(indent + 1)
        return res

    @addToClass(ast.Break)
    def printTree(self, indent=0):
        return indent * separator + " BREAK\n"

    @addToClass(ast.Continue)
    def printTree(self, indent=0):
        return indent * separator + " CONTINUE\n"

    @addToClass(ast.Return)
    def printTree(self, indent=0):
        res = indent * separator + "Return" + "\n"
        res += self.result.printTree(indent + 1)
        return res

    @addToClass(ast.Print)  # 16  skonczone
    def printTree(self, indent=0):
        res = indent * separator + "Print\n"
        res += self.expression.printTree(indent + 1)
        return res

    @addToClass(ast.Access)
    def printTree(self, indent=0):
        res = indent * separator + "REF\n"
        res += (indent + 1) * separator + str(self.variable) + "\n"
        res += self.key.printTree(indent + 1)
        return res

    @addToClass(ast.Error)
    def printTree(self, indent=0):
        return indent * separator + " Error\n"

    @addToClass(ast.Program)
    def printTree(self, indent=0):
        res = ""
        for instruction in self.instructions:
            res += instruction.printTree(indent)
        return res

    @addToClass(ast.Start)
    def printTree(self, indent=0):
        return self.program.printTree(indent)

    @addToClass(ast.Instruction)
    def printTree(self, indent=0):
        return self.line.printTree(indent)

    @addToClass(ast.Matrix)
    def printTree(self, indent=0):
        res = indent * separator + 'MATRIX\n'
        res += self.value.printTree(indent + 1)
        return res

    @addToClass(ast.Rows)
    def printTree(self, indent=0):
        res = ""
        for row in self.row_list:
            res += indent * separator + 'VECTOR\n'
            res += row.printTree(indent + 1)
        return res

    @addToClass(ast.Sequence)
    def printTree(self, indent=0):
        res = ""
        for expression in self.expressions:
            res = expression.printTree(indent)
        return res

    @addToClass(ast.Value)
    def printTree(self, indent=0):
        return indent * separator + str(self.primitive) + "\n"
