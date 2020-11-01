from functools import wraps 
import pickle
from token import Token
from class_ import Class
from astComponents import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens # tokeni od leksera
        self.curr = tokens.pop(0) # trenutni token
        self.prev = None


    def restorable(self, call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__) 
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result
        return wrapper

    # proverava da li je token odgovarajuce klase ako nije baca gresku
    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0) # brise se prvi token iz niza
        else:
            self.die_type(class_.name, self.curr.class_.name) # baca gresku

    
    # u globalnom skoupu var, begin, end, function, procedure
    def program(self):
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == Class.FUNCTION:
                nodes.append(self.function())
            elif self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.procedure())
            elif self.curr.class_ == Class.VAR:
                nodes.append(self.block()) # drugi blok
            elif self.curr.class_ == Class.BEGIN:
                nodes.append(self.block())
            elif self.curr.class_ == Class.END:
                nodes.append(self.block())
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)



    # TODO proveriti
    '''
	fun(arr1[i], arr2[i]);
	y := 5;
    arr[i]
    '''
    def id_(self):
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN and self.is_func_call():
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET and is_array_elem:
            self.eat(Class.LBRACKET)
            index = self.expr()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN: # ako ima dodela vracam id i dodelu
            self.eat(Class.ASSIGN)
            expr = self.expr()
            return Assign(id_, expr)
        else:                           # ako nema vracam samo id
            return id_

    # TODO decl promeniti za niz je drugacije (za niz moze dodela vrednosti kod deklarisanja)
    def decl(self):
        type_ = self.type_()
        id_ = self.id_()
        if self.curr.class_ == Class.LBRACKET:
            self.eat(Class.LBRACKET)
            size = None
            if self.curr.class_ != Class.RBRACKET:
                size = self.expr()
            self.eat(Class.RBRACKET)
            elems = None
            if self.curr.class_ == Class.ASSIGN: # dodela vrednosti nizu = (1, 5, 7+3)
                self.eat(Class.ASSIGN)
                self.eat(Class.LPAREN)
                elems = self.elems()
                self.eat(Class.RPAREN)
            self.eat(Class.SEMICOLON)
            return ArrayDecl(type_, id_, size, elems)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            params = self.params()
            self.eat(Class.RPAREN)
            self.eat(Class.LBRACE)
            block = self.block()
            self.eat(Class.RBRACE)
            return FuncImpl(type_, id_, params, block)
        else:
            self.eat(Class.SEMICOLON)
            return Decl(type_, id_) 

    # citanje funckije
    def function(self):
        self.eat(Class.FUNCTION)
        id_ = self.id_()
        self.eat(Class.LPAREN)
        params = self.params()
        self.eat(Class.RPAREN)
        self.eat(Class.DECL)
        type_ = self.type_()
        self.eat(Class.SEMICOLON)
        #ako ima var blok
        if self.curr.class_ == Class.VAR:
            self.eat(Class.VAR)
            declBlock = self.declBlock()
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        return FuncImpl(type_, id_, params, declBlock, block)

    def procedure(self):
        self.eat(Class.PROCEDURE)
        id_ = self.id_()
        self.eat(Class.LPAREN)
        params = self.params()
        self.eat(Class.RPAREN)
        self.eat(Class.SEMICOLON)
        #ako ima var blok
        if self.curr.class_ == Class.VAR:
            self.eat(Class.VAR)
            declBlock = self.declBlock()
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        return ProcImpl(id_, params, declBlock, block)
        

    def if_(self):
        self.eat(Class.IF)
        cond = self.logic()
        self.eat(Class.THEN)
        self.eat(Class.BEGIN)
        true = self.block()
        self.eat(Class.END)
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            self.eat(Class.BEGIN)
            false = self.block()
            self.eat(Class.END)
        return If(cond, true, false)

    def while_(self):
        self.eat(Class.WHILE)
        cond = self.logic()
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        return While(cond, block)

    def for_(self):
        self.eat(Class.FOR)
        init = self.id_()
        if self.curr.class_ == Class.TO:
            self.eat(Class.TO)
            step = 1
        elif self.curr.class_ == Class.DOWN:
            self.eat(Class.DOWN)
            self.eat(Class.TO)
            step = -1
        limit = self.logic()
        self.eat(Class.DO)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        return For(init, limit, step, block)

    def repeat_until(self):
        self.eat(Class.REPEAT)
        block = self.block()
        self.eat(Class.UNTIL)
        cond = self.logic()
        self.eat(Class.SEMICOLON)
        return RepeatUntil(cond, block)

    def block(self):
        nodes = []
        while self.curr.class_ != Class.END:
            if self.curr.class_ == Class.IF:
                nodes.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.EXIT:
                nodes.append(self.exit())
            # elif self.curr.class_ == Class.TYPE:
            #     nodes.append(self.decl())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            else:
                self.die_deriv(self.block.__name__)
        return Block(nodes)

    def declBlock(self):
        nodes = []
        while self.curr.class_ != Class.BEGIN:  
            nodes.append(self.decl())
        return nodes

    # TODO
    # (argument(s): type1; argument(s): type2; ...)
    def params(self):
        params = {}
        
        while self.curr.class_ != Class.RPAREN:
            # procitam sve idijeve jednog tipa
            ids = []
            currType = None
            if self.curr.class_ == Class.VAR:
                self.eat(Class.VAR)
            while self.curr.class_ != Class.DECL:
                id_ = self.id_
                ids.append(id_)
                if(self.curr.class_ == Class.COMMA):
                    self.eat(Class.COMMA)
            self.eat(Class.DECL)
            currType = self.type_()
            params[currType] = ids  
            if self.curr.class_ == Class.SEMICOLON:
                self.eat(Class.SEMICOLON)
        return Params(params)

    # TODO
    def args(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            args.append(self.expr())
        return Args(args)

    # TODO valjda treba RPAREN  
    def elems(self):
        elems = []
        while self.curr.class_ != Class.RPAREN:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(self.expr())
        return Elems(elems)

    # def return_(self):
    #     self.eat(Class.RETURN)
    #     expr = self.expr()
    #     self.eat(Class.SEMICOLON)
    #     return Return(expr)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def exit(self):
        self.eat(Class.EXIT)
        self.eat(Class.LPAREN)
        expr = self.expr()
        self.eat(Class.RPAREN)
        self.eat(Class.SEMICOLON)
        return Exit(expr)

    def type_(self):
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
        if self.curr.class_ == Class.INTEGER:
            value = Integer(self.curr.lexeme)
            self.eat(Class.INTEGER)
            return value
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.BOOLEAN:
            value = Boolean(self.curr.lexeme)
            self.eat(Class.BOOLEAN)
            return value
        elif self.curr.class_ == Class.REAL:
            value = Real(self.curr.lexeme)
            self.eat(Class.REAL)
            return value
        elif self.curr.class_ == Class.ID:
            return self.id_()
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
            self.eat(Class.RPAREN)
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.FWDSLASH, Class.MOD, Class.DIV]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.DIV:
                op = self.curr.lexeme
                self.eat(Class.DIV)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MOD:
                op = self.curr.lexeme
                self.eat(Class.MOD)
                second = self.factor()
                first = BinOp(op, first, second)
        return first

    def expr(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        first = self.expr()
        if self.curr.class_ == Class.EQ:
            op = self.curr.lexeme
            self.eat(Class.EQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(op, first, second)
        else:
            return first

    def logic(self):
        first = self.compare()
        if self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.OR:
            op = self.curr.lexeme
            self.eat(Class.OR)
            second = self.compare()
            return BinOp(op, first, second)
        else:
            return first

    #proverava da li je poziv funkcije
    @restorable
    def is_func_call(self):
        try:
            self.eat(Class.LPAREN)
            self.args()
            self.eat(Class.RPAREN)
            return self.curr.class_ == Class.SEMICOLON
        except:
            return False

    # ova metoda vraca stablo
    def parse(self):
        return self.program()


    # error handleri
    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die("Derivation error: {}".format(fun))

    def die_type(self, expected, found):
        self.die("Expected: {}, Found: {}".format(expected, found))