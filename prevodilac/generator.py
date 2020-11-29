import re
from grapher import Visitor

# TODO
#? poziv funckija
#? return u funkciji

class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.c = ""
        self.level = 0

    # pomocne funkcije
    def append(self, text): # dodaje string u kod 
        self.c += str(text)

    def newline(self): 
        self.append('\n')

    def indent(self): # uvlacenje
        for i in range(self.level):
            self.append('\t')


    # metode za visit
    def visit_Program(self, parent, node):
        flag = False
        for n in node.nodes:
            if type(n).__name__ == 'MainVarBlock': # ako je usao u glavni var printam main funkciju
                flag = True
            if type(n).__name__ == 'MainBlock': # ako nisam imao var onda za glavni blok stampam int main
                if flag != True:
                    self.append('int main() {')
                    self.newline()
            #print(type(n).__name__)
            self.visit(node, n)
  
    def visit_Decl(self, parent, node):
        self.visit(node, node.type_)
        self.append(' ')
        for i, id in enumerate(node.ids):
            if i > 0:
                self.append(', ')
            self.visit(node, id)
     
    # int niz[5] = {1, 2, 3}

    def visit_ArrayDecl(self, parent, node):
        self.visit(node, node.type_)
        self.append(' ')
        self.visit(node, node.id_)
        lenght = int(node.high.value) - int(node.low.value) + 1
        self.append('[')
        self.append(f'{lenght}')
        self.append(']')
        if node.elems is not None:
            self.append(' = {')
            self.visit(node, node.elems)
            self.append('}')
        
    # char id[len] = {0}
    def visit_stringDecl(self, parent, node):
        for i, id in enumerate(node.ids):
            if i > 0:
                self.indent()
            self.visit(node, node.type_)
            self.append(' ')
            self.visit(node, id)
            self.append('[')
            self.visit(node, node.lenght)
            self.append(']')
            self.append(' = {0}')
            if i != (len(node.ids)-1):
                self.append(';')
                self.newline()
        

    def visit_ArrayElem(self, parent, node):
        self.visit(node, node.id_)
        self.append('[')
        self.visit(node, node.index)
        self.append(']')
        



    def visit_Assign(self, parent, node):
        if type(node.expr).__name__ == 'FuncCall': # ako je 
            if node.expr.id_.value == 'concat':
                self.visit(node, node.expr)
                return
        self.visit(node, node.id_)
        self.append(' = ')
        self.visit(node, node.expr)
           
       

    def visit_If(self, parent, node):
        self.append('if (')
        self.visit(node, node.cond)
        self.append(')')
        self.visit(node, node.true)
        if node.false is not None:
            self.indent()
            self.append('else ')
            self.visit(node, node.false)


    def visit_While(self, parent, node): 
        self.append('while (')
        self.visit(node, node.cond) # cond je BinOp (expr - Operator - drugi expr)
        self.append(')')
        self.newline()
        self.visit(node, node.block)

    # for i := 1 to n do        
    # for (i = 1 ; i <= n ; i++)              
    def visit_For(self, parent, node):
        #? init je assign
        #? cond (op1 - operator - op2) bez ';'
        self.append('for (')
        self.visit(node, node.init) # assign;
        self.append('; ')
        i = node.init.id_.value # promenljiva u cond
        if node.step.value == 1:
            self.visit(node, node.init.id_)
            self.append(' <= ')
            self.visit(node, node.limit) 
            self.append('; ')
            self.append('i = i + 1')
        elif node.step.value == -1:
            self.visit(node, node.init.id_)
            self.append(' >= ')
            self.visit(node, node.limit) 
            self.append('; ')
            self.append('i = i - 1')
        self.append(')')
        self.visit(node, node.block)
        

    def visit_RepeatUntil(self, parent, node): # do while
        self.append('do')
        self.visit(node, node.block)
        self.append(' while (')
        self.visit(node, node.cond)
        self.append(');')

    def visit_FuncImpl(self, parent, node):
        self.visit(node, node.type_)
        self.append(' ')
        self.append(node.id_.value)
        self.append('(')
        self.visit(node, node.params)
        self.append(')')
        self.visit(node, node.block)
        #TODO return od funkcije

    def visit_ProcImpl(self, parent, node):
        self.append('void ')
        self.append(node.id_.value)
        self.append('(')
        self.visit(node, node.params)
        self.append(')')
        self.visit(node, node.block)
        self.newline()


    # TODO ord() ne treba 
    # concat
    # length
    # readln
    # writeln
    # write
    def visit_FuncCall(self, parent, node):
        func = node.id_.value
        args = node.args.args # niz argumenata
        if func == 'write':
            format_ = args[0].value
            matches = re.findall('%[dcs]', format_)
            format_ = re.sub('%[dcs]', '{}', format_)
            self.append('print("')
            self.append(format_)
            self.append('"')
            if len(args) > 1:
                self.append('.format(')
                for i, a in enumerate(args[1:]):
                    if i > 0:
                        self.append(', ')
                    if matches[i] == '%c':
                        self.append('chr(')
                        self.visit(node.args, a)
                        self.append(')')
                    elif matches[i] == '%s':
                        self.append('"".join([chr(x) for x in ')
                        self.visit(node.args, a)
                        self.append('])')
                    else:
                        self.visit(node.args, a)
                self.append(')')
            self.append(', end="")')
        elif func == 'scanf':
            for i, a in enumerate(args[1:]):
                if i > 0:
                    self.append(', ')
                self.visit(node.args, a)
            self.append(' = input()')
            if len(args[1:]) > 1:
                self.append('.split()')
            format_ = args[0].value
            matches = re.findall('%[dcs]', format_)
            for i, m in enumerate(matches):
                if m == '%d':
                    self.newline()
                    self.indent()
                    self.visit(node.args, args[i + 1])
                    self.append(' = int(')
                    self.visit(node.args, args[i + 1])
                    self.append(')')
                elif m == '%c':
                    self.newline()
                    self.indent()
                    self.visit(node.args, args[i + 1])
                    self.append(' = ord(')
                    self.visit(node.args, args[i + 1])
                    self.append('[0])')
                elif m == '%s':
                    self.newline()
                    self.indent()
                    self.visit(node.args, args[i + 1])
                    self.append(' = [ord(x) for x in ')
                    self.visit(node.args, args[i + 1])
                    self.append(']')
        elif func == 'length': # strlen
            self.append('strlen(')
            self.visit(node, node.args)
            self.append(')')
        #strcat(asd, efg);
        #asd := concat(asd, efg);
        elif func == 'concat': # strcat
            self.append('strcat(')
            self.visit(node.args, args[0])
            self.append(', ')
            self.visit(node.args, args[1])
            self.append(')')
            self.indent()
        else:
            self.append(func)
            self.append('(')
            self.visit(node, node.args)
            self.append(')')

    

    def visit_MainBlock(self, parent, node):
        #self.append('int main() {')
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()
        self.append('\r')
        self.append('\treturn 0;\n')
        self.level -= 1
        self.append('}')

    def visit_RepeatBlock(self, parent, node):
        self.append(' {\n')
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()
        self.level -= 1
        self.indent()
        self.append('}')

    

    def visit_Block(self, parent, node):
        self.append(' {\n')
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()
        self.level -= 1
        self.indent()
        self.append('}')
        self.append('\n\r')
        

        

    def visit_MainVarBlock(self, parent, node):
        self.append('int main() {')
        self.level += 1
        self.newline()
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()
        self.level -= 1
        self.append('\r')
        


    def visit_VarBlock(self, parent, node):
        self.level += 1
        self.newline()
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.append(';')
            self.newline()
        self.level -= 1
        self.append('\r')


   
    def visit_Params(self, parent, node):
        for i, (k, v) in enumerate(node.params.items()): # ovde vrv nesto menjati jer je dict
            type_ = k
            ids = v
            for index, id_ in enumerate(ids):
                self.visit(node, type_)
                self.append(' ')
                self.visit(node, id_)
                if index != (len(ids)-1) or i != (len(node.params.items())-1):
                    self.append(', ')
            

    def visit_Args(self, parent, node):
        for i, a in enumerate(node.args):
            if i > 0:
                self.append(', ')
            self.visit(node, a)

    def visit_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            if i > 0:
                self.append(', ')
            self.visit(node, e)

    def visit_Break(self, parent, node):
        self.append('break;')

    def visit_Continue(self, parent, node):
        self.append('continue;')

    def visit_Exit(self, parent, node):
        self.append('return')
        if node.expr is not None:
            self.append(' ')
            self.visit(node, node.expr)

    def visit_Type(self, parent, node):
        if node.value == 'integer':
            self.append('int')
        elif node.value == 'real':
            self.append('float')
        elif node.value == 'boolean':
            self.append('int')
        elif node.value == 'string':
            self.append('char')
        else : 
            self.append(node.value)

    def visit_Integer(self, parent, node):
        self.append(node.value)

    def visit_Char(self, parent, node):
        self.append(f'\'{node.value}\'') # char u c-u je konvertovan u celobrojnu vrednost

    def visit_String(self, parent, node):
        self.append(node.value)

    def visit_Real(self, parent, node):
        self.append(node.value)

    def visit_Boolean(self, parent, node):
        #self.append(node.value)
        if node.value == 'true':
            self.append('1')
        elif node.value == 'false':
            self.append('0')

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_BinOp(self, parent, node): #TODO ako su drugaciji op zameniti
        self.visit(node, node.first)
        self.append(' ')
        if node.symbol == 'and':
            self.append(' && ')
        elif node.symbol == 'or':
            self.append(' || ')
        elif node.symbol == '<>':
            self.append('!=')
        elif node.symbol == '=':
            self.append('==')
        elif node.symbol == 'div':
            self.append('/')
        elif node.symbol == 'mod':
            self.append('%')
        else:
            self.append(node.symbol)
        self.append(' ')
        self.visit(node, node.second)

    def visit_UnOp(self, parent, node): #TODO zameniti opeartore koji su razliciti
        if node.symbol == 'not':
            self.append('!')
        elif node.symbol != '&':
            self.append(node.symbol)
        self.visit(node, node.first)

    def generate(self, path):
        self.visit(None, self.ast) # visit za koren stabla (Program) - rekurzivan poziv (generise kod za svaki cvor)
        self.c = re.sub('\n\s*\n', '\n', self.c) # vise praznih linija menjamo sa jednom linijom
        with open(path, 'w') as source:
            source.write(self.c)
        return path