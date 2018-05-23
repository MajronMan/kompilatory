import ast
import ply.yacc as yacc

from matrix_lexer import MatrixLexer


class MatrixParser:
    tokens = MatrixLexer.tokens

    precedence = (
        ('nonassoc', 'IF'),
        ('nonassoc', 'LESS', 'MORE', 'LESSEQUAL', 'MOREEQUAL', 'ELSE'),
        ('left', 'PLUS', 'MINUS', 'MPLUS', 'MMINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MTIMES', 'MDIVIDE'),
        ('right', 'UMINUS'),
        ('nonassoc', 'TRANSPOSE')
    )

    def p_start(self, p):
        """start : PROGRAM"""
        p[0] = ast.Start(p[1])

    def p_program(self, p):
        """
        PROGRAM : PROGRAM INSTRUCTION
        """
        p[1].instructions.append(p[2])
        p[0] = p[1]

    def p_program_inst(self, p):
        """
        PROGRAM : INSTRUCTION
        """
        p[0] = ast.Program(p[1])

    def p_instruction(self, p):
        """
        INSTRUCTION : STATEMENT SEMICOLON
                    | IF_STATEMENT
                    | WHILE_STATEMENT
                    | FOR_STATEMENT
        """
        p[0] = ast.Instruction(p[1])

    def p_statement(self, p):
        """
        STATEMENT : ASSIGNMENT
                  | KEYWORD
        """
        p[0] = ast.Instruction(p[1])

    def p_assignment(self, p):
        """
        ASSIGNMENT : VARIABLE ASSIGNMENT_OPERATOR EXPRESSION
        """
        p[0] = ast.Assignment(p[1], p[2], p[3])

    def p_variable(self, p):
        """
        VARIABLE : ID
                 | ACCESS
        """
        p[0] = ast.Variable(p[1])

    def p_access(self, p):
        """
        ACCESS : ID LBRACKET SEQUENCE RBRACKET
        """
        p[0] = ast.Access(p[1], p[3])

    def p_sequence(self, p):
        """
        SEQUENCE : SEQUENCE COMMA EXPRESSION                
        """
        p[1].expressions.append(p[3])
        p[0] = p[1]

    def p_sequence_last(self, p):
        """
        SEQUENCE : EXPRESSION
        """
        p[0] = ast.Sequence(p[1])

    def p_value(self, p):
        """
        VALUE : FLOAT
              | INT
              | ID
              | STRING
              | MATRIX
              | ACCESS
        """

        p[0] = ast.Value(p[1])

    def p_matrix(self, p):
        """
        MATRIX : LBRACKET ROWS RBRACKET
        """
        p[0] = ast.MatrixInitializer(p[2])

    def p_rows(self, p):
        """
        ROWS : ROWS SEMICOLON SEQUENCE
        """
        p[1].row_list.append(p[3])
        p[0] = p[1]

    def p_row(self, p):
        """
        ROWS : SEQUENCE
        """
        p[0] = ast.Rows(p[1])

    def p_expression_value(self, p):
        """
        EXPRESSION : VALUE
        """
        p[0] = p[1]

    def p_expression_minus(self, p):
        """
        EXPRESSION : MINUS EXPRESSION %prec UMINUS
        """
        p[0] = ast.Negation(p[2])

    def p_id_transpose(self, p):
        """
        EXPRESSION : ID TRANSPOSE
        """
        p[0] = ast.Transposition(ast.Variable(p[1]))

    def p_expression_transpose(self, p):
        """
        EXPRESSION : LPAREN EXPRESSION RPAREN TRANSPOSE
        """
        p[0] = ast.Transposition(p[2])

    def p_expression_paren(self, p):
        """
        EXPRESSION : LPAREN EXPRESSION RPAREN
        """
        p[0] = p[2]

    def p_expression_math(self, p):
        """
        EXPRESSION : EXPRESSION PLUS EXPRESSION
                   | EXPRESSION MINUS EXPRESSION
                   | EXPRESSION TIMES EXPRESSION
                   | EXPRESSION DIVIDE EXPRESSION
                   | EXPRESSION MPLUS EXPRESSION
                   | EXPRESSION MMINUS EXPRESSION
                   | EXPRESSION MTIMES EXPRESSION
                   | EXPRESSION MDIVIDE EXPRESSION
        """
        p[0] = ast.BinaryExpression(p[1], p[2], p[3])

    def p_expression_fun(self, p):
        """
        EXPRESSION : FUNCTION LPAREN EXPRESSION RPAREN
        """
        p[0] = ast.Function(p[1], p[3])

    def p_keyword_print(self, p):
        """
        KEYWORD : PRINT SEQUENCE
        """
        p[0] = ast.Print(p[2])

    def p_keyword_break(self, p):
        """
        KEYWORD : BREAK
        """
        p[0] = ast.Break()

    def p_keyword_continue(self, p):
        """
        KEYWORD : CONTINUE
        """
        p[0] = ast.Continue()

    def p_keyword_return(self, p):
        """
        KEYWORD : RETURN
        """
        p[0] = ast.Return(p[2])

    def p_relation(self, p):
        """RELATION : EXPRESSION COMPARISION_OPERATOR EXPRESSION"""
        p[0] = ast.BinaryExpression(p[1], p[2], p[3])

    def p_body(self, p):
        """BODY : INSTRUCTION"""
        p[0] = ast.Instruction(p[1])

    def p_body_curly(self, p):
        """BODY : LCURLY PROGRAM RCURLY"""
        p[0] = ast.Instruction(p[2])

    def p_if_statement(self, p):
        """
        IF_STATEMENT : IF LPAREN RELATION RPAREN BODY %prec IF
        """
        p[0] = ast.If(p[3], p[5])

    def p_if_else_statement(self, p):
        """
        IF_STATEMENT : IF LPAREN RELATION RPAREN BODY ELSE BODY
        """
        p[0] = ast.If(p[3], p[5], p[7])

    def p_while_statement(self, p):
        """WHILE_STATEMENT : WHILE LPAREN RELATION RPAREN BODY"""
        p[0] = ast.While(p[3], p[5])

    def p_for_statement(self, p):
        """FOR_STATEMENT : FOR ID ASSIGN RANGE BODY"""
        p[0] = ast.For(p[2], p[4], p[5])

    def p_range(self, p):
        """RANGE : EXPRESSION COLON EXPRESSION"""
        p[0] = ast.Range(p[1], p[3])

    def p_range_step(self, p):
        """
         RANGE : EXPRESSION COLON EXPRESSION COLON EXPRESSION
        """
        p[0] = ast.Range(p[1], p[3], p[5])

    def p_assignment_operator(self, p):
        """
        ASSIGNMENT_OPERATOR : ASSIGN
                            | PLUSASSIGN
                            | MINUSASSIGN
                            | TIMESASSIGN
                            | DIVIDEASSIGN
        """
        p[0] = p[1]

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

    def p_function(self, p):
        """
        FUNCTION : EYE
                 | ZEROS
                 | ONES
        """
        p[0] = p[1]

    def p_error(self, p):
        print('/' * 40 + 'ERROR\nIllegal symbol {}\n'.format(p.value) + '/' * 40)

    def __init__(self):
        self.parser = None
        self.matrix_lexer = MatrixLexer()

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self)

    def run(self, s, **kwargs):
        self.build(**kwargs)
        self.matrix_lexer.run(s, **kwargs)
        self.matrix_lexer.print_result()
        self.parser.parse(s, lexer=self.matrix_lexer.lexer)
