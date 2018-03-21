import unittest 
import re 

from matrix_lexer import MatrixLexer

def normalize(output):
  return list(
    map(
      lambda x: x.strip(), 
      filter(
        lambda y: not re.match(empty_line, y), 
        output.split('\n'))
    )
  )

empty_line = re.compile(r'^\s*$')

class TestMatrixLexer(unittest.TestCase):
  def test_basic(self):
    s = "a = (2 + 2 * 2) / 2.0 # Simple"

    expected = normalize("""
      (1, 0): ID(a)
      (1, 2): ASSIGN(=)
      (1, 4): LPAREN(()
      (1, 5): INT(2)
      (1, 7): PLUS(+)
      (1, 9): INT(2)
      (1, 11): TIMES(*)
      (1, 13): INT(2)
      (1, 14): RPAREN())
      (1, 16): DIVIDE(/)
      (1, 18): FLOAT(2.0)
      """)

    lexer = MatrixLexer()
    lexer.run(s)

    result = normalize(lexer.show_result())
    self.assertEqual(result, expected)


  def test_from_lab(self):
    s = ( "A = zeros(5); # create 5x5 matrix filled with zeros\n" +
          "B = ones(7);  # create 7x7 matrix filled with ones\n" +
          "I = eye(10);  # create 10x10 matrix filled with ones on diagonal and zeros elsewhere\n" +
          "D1 = A.+B' ;  # add element-wise A with transpose of B\n" +
          "D2 -= A.-B';  # substract element-wise A with transpose of B\n" +
          "D3 *= A.*B';  # multiply element-wise A with transpose of B\n" +
          "D4 /= A./B';  # divide element-wise A with transpose of B\n")

    expected = normalize("""
      (1, 0): ID(A)
      (1, 2): ASSIGN(=)
      (1, 4): ZEROS(zeros)
      (1, 9): LPAREN(()
      (1, 10): INT(5)
      (1, 11): RPAREN())
      (1, 12): SEMICOLON(;)
      (2, 1): ID(B)
      (2, 3): ASSIGN(=)
      (2, 5): ONES(ones)
      (2, 9): LPAREN(()
      (2, 10): INT(7)
      (2, 11): RPAREN())
      (2, 12): SEMICOLON(;)
      (3, 1): ID(I)
      (3, 3): ASSIGN(=)
      (3, 5): EYE(eye)
      (3, 8): LPAREN(()
      (3, 9): INT(10)
      (3, 11): RPAREN())
      (3, 12): SEMICOLON(;)
      (4, 1): ID(D1)
      (4, 4): ASSIGN(=)
      (4, 6): ID(A)
      (4, 7): MPLUS(.+)
      (4, 9): ID(B)
      (4, 10): TRANSPOSE(')
      (4, 12): SEMICOLON(;)
      (5, 1): ID(D2)
      (5, 4): MINUSASSIGN(-=)
      (5, 7): ID(A)
      (5, 8): MMINUS(.-)
      (5, 10): ID(B)
      (5, 11): TRANSPOSE(')
      (5, 12): SEMICOLON(;)
      (6, 1): ID(D3)
      (6, 4): TIMESASSIGN(*=)
      (6, 7): ID(A)
      (6, 8): MTIMES(.*)
      (6, 10): ID(B)
      (6, 11): TRANSPOSE(')
      (6, 12): SEMICOLON(;)
      (7, 1): ID(D4)
      (7, 4): DIVIDEASSIGN(/=)
      (7, 7): ID(A)
      (7, 8): MDIVIDE(./)
      (7, 10): ID(B)
      (7, 11): TRANSPOSE(')
      (7, 12): SEMICOLON(;)
    """)

    lexer = MatrixLexer()
    lexer.run(s)

    result = normalize(lexer.show_result())
    self.assertEqual(result, expected)

if __name__ == "__main__":
  unittest.main()
