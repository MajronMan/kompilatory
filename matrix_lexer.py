import ply.lex as lex


class ColumnCounter:
    newlines = [0]

    @staticmethod
    def get_column(t):
        # Lines start at 1 not 0
        return t.lexpos - ColumnCounter.newlines[t.lineno - 1]

    @staticmethod
    def add_newline(t):
        for i in range(len(t.value)):
            ColumnCounter.newlines.append(t.lexpos + i)


class MatrixLexer:
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT',
    }

    tokens = [
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'MPLUS',
                 'MMINUS',
                 'MTIMES',
                 'MDIVIDE',
                 'ASSIGN',
                 'PLUSASSIGN',
                 'MINUSASSIGN',
                 'TIMESASSIGN',
                 'DIVIDEASSIGN',
                 'LESS',
                 'MORE',
                 'LESSEQUAL',
                 'MOREEQUAL',
                 'INEQUAL',
                 'EQUAL',
                 'LPAREN',
                 'RPAREN',
                 'LBRACKET',
                 'RBRACKET',
                 'LCURLY',
                 'RCURLY',
                 'COLON',
                 'TRANSPOSE',
                 'COMMA',
                 'SEMICOLON',
                 'ID',
                 'INT',
                 'FLOAT',
                 'STRING'
             ] + list(reserved.values())

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MPLUS = r'\.\+'
    t_MMINUS = r'\.-'
    t_MTIMES = r'\.\*'
    t_MDIVIDE = r'\./'
    t_ASSIGN = r'='
    t_PLUSASSIGN = r'\+='
    t_MINUSASSIGN = r'-='
    t_TIMESASSIGN = r'\*='
    t_DIVIDEASSIGN = r'/='
    t_LESS = r'<'
    t_MORE = r'>'
    t_LESSEQUAL = r'<='
    t_MOREEQUAL = r'>='
    t_INEQUAL = r'!='
    t_EQUAL = r'=='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_COLON = r':'
    t_TRANSPOSE = r'\''
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_STRING = r'"[^"]*"'

    t_ignore = ' \t'
    t_ignore_COMMENT = r'\#.*'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_FLOAT(self, t):
        r'\d*\.\d+'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        ColumnCounter.add_newline(t)

    def t_error(self, t):
        print("illegal character '%s' at (%d, %d)" %
              (t.value[0], t.lineno, ColumnCounter.get_column(t)))
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = None
        self.result = []

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def show_token(self, token):
        return "(%d, %d): %s(%s)" % (
            token.lineno,
            ColumnCounter.get_column(token),
            token.type,
            token.value
        )

    def run(self, s, **kwargs):
        self.build(**kwargs)
        self.lexer.input(s)
        for token in self.lexer:
            self.result.append(token)

    def show_result(self):
        result = ""
        for token in self.result:
            result += self.show_token(token) + "\n"
        return result

    def print_result(self):
        print(self.show_result())
