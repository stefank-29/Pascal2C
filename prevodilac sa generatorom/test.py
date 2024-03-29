from lexer import Lexer
from parser import Parser
from generator import Generator
#from grapher import *
id = '15'
path = f'./Datoteke/Druga faza/{id}/src.pas'
with open(path, 'r') as source:
    text = source.read()
    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    ast = parser.parse()

    generator = Generator(ast)
    code = generator.generate('main.c') # ime fajla
    #print(code)


#grapher = Grapher(ast)
#img = grapher.graph()
# Image(img) 
# print(ast)
# for t in tokens:
#     print(t)



