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
        res += self.expression.printTree(indent + 1)
        return res

    @addToClass(ast.Negation)
    def printTree(self, indent=0):
        res = indent * separator + "Negation\n"
        res += self.operand.printTree(indent + 1)
        return res

    @addToClass(ast.Transposition)
    def printTree(self, indent=0):
        res = indent * separator + "Transposition\n"
        res += self.operand.printTree(indent + 1)
        return res

    @addToClass(ast.Assignment)
    def printTree(self, indent=0):
        res = indent * separator + str(self.operator) + '\n'
        res += self.left.printTree(indent + 1)
        res += self.right.printTree(indent + 1)

        return res

    @addToClass(ast.Function)
    def printTree(self, indent=0):
        res = indent * separator + str(self.name) + '\n'
        res += self.argument.printTree(indent + 1)
        return res

    @addToClass(ast.Variable)
    def printTree(self, indent=0):
        if issubclass(type(self.name), ast.Node):
            return self.name.printTree(indent)
        return indent * separator + str(self.name) + '\n'

    @addToClass(ast.If)
    def printTree(self, indent=0):
        res = indent * separator + "IF\n"
        res += self.condition.printTree(indent + 1)
        res += indent * separator + "THEN\n"
        res += self.expression.printTree(indent + 1)
        if (self.else_expression != None):
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
        res = indent * separator + "RANGE\n"
        res += self.start.printTree(indent + 1)
        res += self.end.printTree(indent + 1)
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

    @addToClass(ast.Instructions)
    def printTree(self, indent=0):
        res = ""
        if self.instructions:
            res += self.instructions.printTree(indent)
        res += self.instruction.printTree(indent)
        return res

    @addToClass(ast.Start)
    def printTree(self, indent=0):
        return self.instructions.printTree(indent)

    @addToClass(ast.Instruction)
    def printTree(self, indent=0):
        return self.instruction.printTree(indent)

    @addToClass(ast.MatrixInitializer)
    def printTree(self, indent=0):
        res = indent * separator + 'MATRIX\n'
        res += self.instruction.printTree(indent + 1)
        return res

    @addToClass(ast.Value)
    def printTree(self, indent=0):
        if issubclass(type(self.value), ast.Node):
            return self.value.printTree(indent)
        return indent * separator + str(self.value) + '\n'

    @addToClass(ast.Rows)
    def printTree(self, indent=0):
        res = ""
        for row in self.row_list:
            res += indent * separator + 'VECTOR\n'
            res += row.printTree(indent + 1)
        return res

    @addToClass(ast.Sequence)
    def printTree(self, indent=0):
        res = self.sequence.printTree(indent)
        res += self.expression.printTree(indent)

        return res
