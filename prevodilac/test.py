from lexer import Lexer
from parser import Parser

test_id = 1
path = './pas/test3.pas'
with open(path, 'r') as source:
    text = source.read()

    lexer = Lexer(text)
    tokens = lexer.lex()

    # parser = Parser(tokens)
    # ast = parser.parse()


    for t in tokens:
        print(t)
