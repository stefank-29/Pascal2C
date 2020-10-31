from lexer import Lexer

test_id = 1
path = './pas/test6.pas'
with open(path, 'r') as source:
    text = source.read()

    lexer = Lexer(text)
    tokens = lexer.lex()

    for t in tokens:
        print(t)
