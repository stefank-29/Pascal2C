from lexer import Lexer
from parser import Parser
from generator import Generator
#from grapher import *

path = './pas/test3.pas'
with open(path, 'r') as source:
    text = source.read()
    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()

    generator = Generator(ast)
    code = generator.generate('main.py')

    print(code)
#grapher = Grapher(ast)
#img = grapher.graph()
# Image(img) 
# print(ast)
# for t in tokens:
#     print(t)



#TODO za for id vraca i id i expr (treba odvojeno da ih sacuvam)