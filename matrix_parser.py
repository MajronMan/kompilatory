import ast
import ply.yacc as yacc
from matrix_lexer import MatrixLexer


class MatrixParser:
    tokens = MatrixLexer.tokens

    precedence = (
        ('nonassoc', 'LESS', 'MORE', 'LESSEQUAL', 'MOREEQUAL', 'IF', 'ELSE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS')
    )

    def p_start(self, p):
        """start : PROGRAM"""
        p[0] = p[1]
        print('p_start: {}'.format(p[0]))

    def p_program(self, p):
        """
        PROGRAM : PROGRAM INSTRUCTION
                | INSTRUCTION
        """
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        print('p_program: {}'.format(p[0]))

    def p_instruction(self, p):
        """
        INSTRUCTION : STATEMENT SEMICOLON
                    | IF_STATEMENT
                    | WHILE_STATEMENT
                    | FOR_STATEMENT
        """
        p[0] = p[1]
        print('p_instruction: {}'.format(p[0]))

    def p_statement(self, p):
        """
        STATEMENT : ASSIGNMENT
                  | KEYWORD
        """
        p[0] = p[1]
        print('p_statement: {}'.format(p[0]))

    def p_assignment(self, p):
        """
        ASSIGNMENT : VARIABLE ASSIGNMENT_OPERATOR EXPRESSION
        """
        p[0] = ast.Assignment(p[1], p[2], p[3])
        print('p_assignment: {}'.format(p[0]))

    def p_variable(self, p):
        """
        VARIABLE : ID
                 | ACCESS
        """
        p[0] = ast.Variable(p[1])
        print('p_variable: {}'.format(p[0]))

    def p_access(self, p):
        """
        ACCESS : ID LBRACKET SEQUENCE RBRACKET
        """
        p[0] = ast.Access(p[1], p[3])
        print('p_access: {}'.format(p[0]))

    def p_sequence(self, p):
        """
        SEQUENCE : SEQUENCE COMMA EXPRESSION
                 | EXPRESSION
        """
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        print('p_sequence: {}'.format(p[0]))

    def p_value(self, p):
        """
        VALUE : FLOAT
              | INT
              | ID
              | STRING
              | MATRIX
              | ACCESS
        """
        p[0] = p[1]
        print('p_value: {}'.format(p[0]))

    def p_matrix(self, p):
        """
        MATRIX : LBRACKET ROWS RBRACKET
        """
        p[0] = p[2]
        print('p_matrix: {}'.format(p[0]))

    def p_rows(self, p):
        """
        ROWS : ROWS SEMICOLON SEQUENCE
             | SEQUENCE
        """
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        print('p_rows: {}'.format(p[0]))

    def p_expression(self, p):
        """
        EXPRESSION : VALUE
                   | MINUS EXPRESSION %prec UMINUS
                   | EXPRESSION TRANSPOSE
                   | LPAREN EXPRESSION RPAREN
                   | EXPRESSION MATHEMATICAL_OPERATOR EXPRESSION
                   | FUNCTION LPAREN EXPRESSION RPAREN
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3 and p[1] == '-':
            p[0] = ast.Negation(p[2])
        elif len(p) == 3 and p[2] == '\'':
            p[0] = ast.Transposition(p[1])
        elif len(p) == 4 and p[1] == '(' and p[3] == ')':
            p[0] = p[2]
        elif len(p) == 5 and p[2] == '(' and p[4] == ')':
            p[0] = ast.Function(p[1], p[3])
        elif len(p) == 4:
            p[0] = ast.BinaryExpression(p[1], p[2], p[3])
        print('p_expression: {}'.format(p[0]))

    def p_keyword(self, p):
        """KEYWORD : PRINT SEQUENCE
                   | BREAK
                   | CONTINUE
                   | RETURN EXPRESSION"""
        if p[1] == 'print':
            p[0] = ast.Print(p[2])
        elif p[1] == 'return':
            p[0] = ast.Return(p[2])
        elif p[1] == 'break':
            p[0] = ast.Break()
        elif p[1] == 'continue':
            p[0] = ast.Continue()
        print('p_keyword: {}'.format(p[0]))

    def p_relation(self, p):
        """RELATION : EXPRESSION COMPARISION_OPERATOR EXPRESSION"""
        p[0] = ast.Relation(p[1], p[2], p[3])
        print('p_relation: {}'.format(p[0]))

    def p_body(self, p):
        """BODY : LCURLY PROGRAM RCURLY
                | INSTRUCTION"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[2]
        print('p_body: {}'.format(p[0]))

    def p_if_statement(self, p):
        """IF_STATEMENT : IF LPAREN RELATION RPAREN BODY
                        | IF LPAREN RELATION RPAREN BODY ELSE BODY"""
        if len(p) == 8:
            p[0] = ast.If(p[3], p[5], p[7])
        elif len(p) == 6:
            p[0] = ast.If(p[3], p[5])
        print('p_if_statement: {}'.format(p[0]))

    def p_while_statement(self, p):
        """WHILE_STATEMENT : WHILE LPAREN RELATION RPAREN BODY"""
        p[0] = ast.While(p[3], p[5])
        print('p_while_statement: {}'.format(p[0]))

    def p_for_statement(self, p):
        """FOR_STATEMENT : FOR ID ASSIGN RANGE BODY"""
        p[0] = ast.For(p[2], p[4], p[5])
        print('p_for_statement: {}'.format(p[0]))

    def p_range(self, p):
        """RANGE : EXPRESSION COLON EXPRESSION
                 | EXPRESSION COLON EXPRESSION COLON EXPRESSION"""
        if len(p) == 4:
            p[0] = ast.Range(p[1], p[3])
        elif len(p) == 6:
            p[0] = ast.Range(p[1], p[3], p[5])
        print('p_range: {}'.format(p[0]))

    def p_assignment_operator(self, p):
        """
        ASSIGNMENT_OPERATOR : ASSIGN
                            | PLUSASSIGN
                            | MINUSASSIGN
                            | TIMESASSIGN
                            | DIVIDEASSIGN
        """
        p[0] = p[1]
        print('p_assignment_operator: {}'.format(p[0]))

    def p_comparision_operator(self, p):
        """
        COMPARISION_OPERATOR : LESS
                             | MORE
                             | EQUAL
                             | INEQUAL
                             | LESSEQUAL
                             | MOREEQUAL
        """
        p[0] = p[1]
        print('p_comparision_operator: {}'.format(p[0]))

    def p_mathematical_operator(self, p):
        """
        MATHEMATICAL_OPERATOR : PLUS
                              | MINUS
                              | TIMES
                              | DIVIDE
                              | MPLUS
                              | MMINUS
                              | MTIMES
                              | MDIVIDE
        """
        p[0] = p[1]
        print('p_mathematical_operator: {}'.format(p[0]))

    def p_function(self, p):
        """
        FUNCTION : EYE
                 | ZEROS
                 | ONES
        """
        p[0] = p[1]
        print('p_function: {}'.format(p[0]))

    def p_error(self, p):
        print('/' * 40 + 'ERROR\nIllegal symbol {}\n'.format(p.value) + '/' * 40)

    def __init__(self):
        self.parser = None

    def build(self, **kwargs):
        self.matrix_lexer = MatrixLexer()
        self.parser = yacc.yacc(module=self)

    def run(self, s, **kwargs):
        self.build(**kwargs)
        self.matrix_lexer.run(s, **kwargs)
        self.matrix_lexer.print_result()
        self.parser.parse(s, lexer=self.matrix_lexer.lexer)
