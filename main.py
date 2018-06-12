import sys
import ply.yacc as yacc
import TreePrinter
from Interpreter import Interpreter
from type_checker import TypeChecker

from matrix_parser import MatrixParser

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example/example1.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(1)

    MatrixParser = MatrixParser()
    parser = yacc.yacc(module=MatrixParser)
    text = file.read()
    ast = parser.parse(text, lexer=MatrixParser.matrix_lexer)
    if MatrixParser.error or not parser.errorok:
        sys.exit(1)
    tc = TypeChecker()
    tc.visit(ast)

    interpreter = Interpreter()
    interpreter.visit(ast)
    #print(ast.printTree())

    #list(map(print, tc.errors))

