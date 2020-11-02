from lexer import Lexer
from parser import Parser
from grapher import *



test_id = 1
path = './pas/test2.pas'
with open(path, 'r') as source:
    text = source.read()

    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()

    grapher = Grapher(ast)
    img = grapher.graph()
    
Image(img)
    
#print(ast)

# for t in tokens:
#     print(t)
