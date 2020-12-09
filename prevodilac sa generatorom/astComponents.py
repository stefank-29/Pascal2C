class Node():
    pass


class Program(Node):
    def __init__(self, nodes): # niz node-ova koje ima glavni program
        self.nodes = nodes

'''
- deklaracija
- x, y: string;
ne cuva se ; jer je to sintaksa
'''
class Decl(Node):
    def __init__(self, type_, ids):
        self.type_ = type_
        self.ids = ids

class stringDecl(Node):
    def __init__(self, type_, ids, lenght):
        self.type_ = type_
        self.ids = ids
        self.lenght = lenght

''' 
-cuva se tip, id, velicina, elementi 
arr2: array [1..3] of integer = (1, 23, 456);
size = high - low + 1
'''
class ArrayDecl(Node):
    def __init__(self, type_, ids, low, high, elems):
        self.type_ = type_
        self.ids = ids
        self.low = low
        self.high = high
        self.elems = elems
        
'''
-get array element
-> arr[i]
'''
class ArrayElem(Node):
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index

'''
x:= 5
x:= 5 + 2 * 3
'''
class Assign(Node):
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr

# uslov, blok kada je uslov ispunjen, blok kada nije ispunjen
class If(Node):
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false

# uslov, kod
# while (condition) do block;
class While(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

'''
for < variable-name > := < initial_value > to [down to] < final_value > do 
   block;
init - cond - step(inc or dec), block;
'''
class For(Node):
    def __init__(self, init, limit, step, block):
        self.init = init
        self.limit = limit
        self.step = step
        self.block = block

# block - cond
class RepeatUntil(Node):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

'''
- tip naziv parametri blok koda
- nema return nego se nazivu fje dodeli vrednost koja se vraca ili exit(vrednost)
'''
class FuncImpl(Node):
    def __init__(self, type_, id_, params, declBlock, block):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.declBlock = declBlock
        self.block = block

# naziv fje i argumenti koji se prosledjuju
class FuncCall(Node):
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args

class ProcImpl(Node):
    def __init__(self, id_, params, declBlock, block):
        self.id_ = id_
        self.params = params
        self.declBlock = declBlock
        self.block = block

# class ProcCall(Node):
#     def __init__(self, id_, args):
#         self.id_ = id_
#         self.args = args   

# blok sa deklaracijama
class MainVarBlock(Node):
    def __init__(self, nodes):
        self.nodes = nodes

class VarBlock(Node):
    def __init__(self, nodes):
        self.nodes = nodes

class RepeatBlock(Node):
    def __init__(self, nodes):
        self.nodes = nodes

class MainBlock(Node):
    def __init__(self, nodes):
        self.nodes = nodes
        
class FuncBlock(Node):
    def __init__(self, nodes):
        self.nodes = nodes
        
# blok sadrzi niz node-ova
class Block(Node):
    def __init__(self, nodes):
        self.nodes = nodes

# parametri (niz deklaracija (Decl))
class Params(Node):
    def __init__(self, params):
        self.params = params

# argumenti
class Args(Node):
    def __init__(self, args):
        self.args = args

# elementi niza (arr2: array [1..3] of integer = (1, 23, 456);)
class Elems(Node):
    def __init__(self, elems):
        self.elems = elems

 
class Break(Node):
    pass


class Continue(Node):
    pass

# moze da vraca vrednost iz f-je nalik return-u
class Exit(Node):
    def __init__(self, expr):
        self.expr = expr


# class Return(Node):
#     def __init__(self, expr):
#         self.expr = expr

# integer, char, string, real, boolean
class Type(Node):
    def __init__(self, value):
        self.value = value




class Integer(Node):
    def __init__(self, value):
        self.value = value





class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value

class Real(Node):
    def __init__(self, value):
        self.value = value

class Boolean(Node):
    def __init__(self, value):
        self.value = value

# naziv promenljive
class Id(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second

class BinOpPar(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second

class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first

class UnOpPar(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first