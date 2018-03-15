import sys
import ply.lex as lex

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
    'eye' : 'EYE' ,
    'zeroes' :'ZEROS',
    'ones' : 'ONES',
    'print' : 'PRINT',
}

tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'NUMBER',
    'ID',
]+ list(reserved.values())




t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EYE = r'eye'
t_ZEROS = r'zeros'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)


lexer = lex.lex()
fh = None
try:
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "example.txt", "r");
    lexer.input( fh.read() )
    for token in lexer:
        print("line %d: %s(%s)" %(token.lineno, token.type, token.value))
except:
    print("open error\n")