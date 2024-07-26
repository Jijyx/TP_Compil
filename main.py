from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ('NAME', 'NUMBER', 'OPERATOR', 'PARENTHESES')


# --- Compteurs de chaques variables et opérateurs

c_PARENTHESES = 0
c_NAME = 0
c_NUMBER = 0
c_OPERATORS = 0


# Ignored characters
t_ignore = ' \t'


# quand un token est trouvé, on incrémente le compteur correspondant
# on crée donc une fonction qui renvoie le token et incrémente le compteur
def t_OPERATOR(t):
    r'[\+\-\*\/\=]'
    global c_OPERATORS
    c_OPERATORS += 1
    return t

def t_PARENTHESES(t):
    r'[\(\)]'
    global c_PARENTHESES
    c_PARENTHESES += 1
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    global c_NAME
    c_NAME += 1
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    global c_NUMBER
    c_NUMBER += 1
    return t

# si on veut ignorer les nouvelles lignes
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# si on connait pas le token on affiche un message d'erreur
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()

# --- 

#   expression : facor OPERATOR factor
#              | factor
#
#
#   factor     : NAME
#              | NUMBER
#              | OPERATOR factor
#              | PARENTHESES expression PARENTHESES
#              

# x = 3 * (4 + y)


def p_expression_factor_operator(p):
    '''
    expression : expression OPERATOR expression
    '''
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_factor(p):
    '''
    expression : factor
    '''
    p[0] = p[1]


def p_factor_name(p):   
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])


def p_factor_number(p): 
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])


# def p_factor_operator(p): 
#     '''
#     factor : OPERATOR factor
#     '''
#     print('factor_operator')
#     p[0] = ('operator', p[1], p[2])


def p_factor_grouped(p):
    '''
    factor : PARENTHESES expression PARENTHESES
    '''   
    p[0] = ('factor_grouped', p[2])


def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# on parse le code
banane = parser.parse('x = 3 * (4 + y)')
# on affiche le nombre de tokens de chaque type
print(banane)
print(f'NAME: {c_NAME}')
print(f'NUMBER: {c_NUMBER}')
print(f'OPERATORS: {c_OPERATORS}')
print(f'PARENTHESES: {c_PARENTHESES}')