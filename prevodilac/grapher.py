#from graphviz import Digraph, Source
#from IPython.display import Image

# TODO za svaku klasu iz astComponents treba da ima odgovarajucu visit metodu

class Visitor():
    def visit(self, parent, node): #? prima cvor i roditelja
        method = 'visit_' + type(node).__name__ #? kreiram metodu (type vraca klasu)
        visitor = getattr(self, method, self.die) #? iz grafera dobijamo metodu sa tim imenom
        return visitor(parent, node)

    def die(self, parent, node):
        method = 'visit_' + type(node).__name__
        raise SystemExit("Missing method: {}".format(method))



class Grapher(Visitor):
    def __init__(self, ast):
        self.ast = ast # stablo
        self._count = 1 # brojac cvorova
        self.dot = Digraph() # kreiranje grafa (usmeren)
        self.dot.node_attr['shape'] = 'box'
        self.dot.node_attr['height'] = '0.1'
        self.dot.edge_attr['arrowsize'] = '0.5'

    def add_node(self, parent, node, name=None):
        node._index = self._count   # jedinstveni id
        self._count += 1
        caption = type(node).__name__ # labela
        if name is not None:
            caption = '{} : {}'.format(caption, name) # dodatna informacija
        self.dot.node('node{}'.format(node._index), caption) # dodaje se node
        if parent is not None: # dodaje se veza izmedju roditelja i deteta
            self.add_edge(parent, node)

    def add_edge(self, parent, node):
        src, dest = parent._index, node._index
        self.dot.edge('node{}'.format(src), 'node{}'.format(dest))


    # TODO odavde dodati sve sto treba i proveriti
    def visit_Program(self, parent, node):
        self.add_node(parent, node)
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.type_) # obidje se tip
        for id_ in node.ids:        # obidju se id-jevu
            self.visit(node, id_)

    def visit_stringDecl(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.type_) # obidje se tip
        for id_ in node.ids:        # obidju se id-jevu
            self.visit(node, id_)
        self.visit(node, node.lenght)


    def visit_ArrayDecl(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.type_)
        self.visit(node, node.id_)
        self.visit(node, node.low)
        self.visit(node, node.high)
        if node.elems is not None:
            self.visit(node, node.elems)

    def visit_ArrayElem(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.id_)
        self.visit(node, node.index)

    # x := 5;
    def visit_Assign(self, parent, node):
        self.add_node(parent, node) # dodaje se taj cvor
        self.visit(node, node.id_) # dodaje se cvor za x
        self.visit(node, node.expr) # dodaje se cvor za 5

    def visit_If(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.cond)
        self.visit(node, node.true)
        if node.false is not None:
            self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.cond)
        self.visit(node, node.block)

    def visit_For(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.init)
        self.visit(node, node.limit)
        self.visit(node, node.step)
        self.visit(node, node.block)

    def visit_RepeatUntil(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.cond)
        self.visit(node, node.block)


    def visit_FuncImpl(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.type_)
        self.visit(node, node.id_)
        self.visit(node, node.params)
        if node.declBlock is not None:
          self.visit(node, node.declBlock)
        self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.id_)
        self.visit(node, node.args)

    def visit_ProcImpl(self, parent, node):
        self.add_node(parent, node)
        self.visit(node, node.id_)
        self.visit(node, node.params)
        if node.declBlock is not None:
          self.visit(node, node.declBlock)
        self.visit(node, node.block)

    def visit_Block(self, parent, node):
        self.add_node(parent, node)
        for n in node.nodes:
            self.visit(node, n)

    def visit_VarBlock(self, parent, node):
        self.add_node(parent, node)
        for n in node.nodes:
            self.visit(node, n)

    def visit_Params(self, parent, node):
        self.add_node(parent, node)
        for key in node.params.keys():
            self.visit(node, key)
            for id in node.params[key]:
              self.visit(node, id)
            # id za key

    def visit_Args(self, parent, node):
        self.add_node(parent, node)
        for a in node.args:
            self.visit(node, a)

    def visit_Elems(self, parent, node):
        self.add_node(parent, node)
        for e in node.elems:
            self.visit(node, e)

    def visit_Break(self, parent, node):
        self.add_node(parent, node)

    def visit_Continue(self, parent, node):
        self.add_node(parent, node)

    def visit_Exit(self, parent, node):
        self.add_node(parent, node)
        if node.expr is not None:
            self.visit(node, node.expr)

    def visit_Type(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Integer(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_int(self, parent, node):
        print(node)
        # name = node.value
        # self.add_node(parent, node, name)

    def visit_Char(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_String(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Real(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Boolean(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Id(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_BinOp(self, parent, node):
        name = node.symbol
        self.add_node(parent, node, name)
        self.visit(node, node.first)
        self.visit(node, node.second)

    def visit_UnOp(self, parent, node):
        name = node.symbol
        self.add_node(parent, node, name)
        self.visit(node, node.first)

    # posecuje trenutni cvor i roditelja (koren nema roditelja)
    def graph(self):
        self.visit(None, self.ast)
        s = Source(self.dot.source, filename='graph', format='png')
        return s.view()