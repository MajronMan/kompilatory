import sys
from matrix_lexer import MatrixLexer


if __name__ == "__main__":
  lexer = MatrixLexer()
  filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
  with open(filename, 'r') as f:
    lexer.run(f.read())
    lexer.print_result()
