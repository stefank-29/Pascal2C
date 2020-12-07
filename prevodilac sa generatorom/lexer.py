from token import Token
from class_ import Class


class Lexer:
    def __init__(self, text):
        self.text = text
        self.len = len(text)
        self.pos = -1

    def read_space(self):
        while self.pos + 1 < self.len and self.text[self.pos + 1].isspace():
            self.next_char()

    def read_int(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and (self.text[self.pos + 1].isdigit() or ('.' not in lexeme and self.text[self.pos + 1] == '.' and self.text[self.pos + 2] != '.')):
            lexeme += self.next_char()
        # if '.' not in lexeme:
        #     return int(lexeme)
        # else:
        #     return (lexeme)
        return lexeme

    def read_char(self):
        self.pos += 1
        lexeme = self.text[self.pos]
        self.pos += 1
        return lexeme

    def read_string(self):
        lexeme = ''
        while self.pos + 1 < self.len and self.text[self.pos + 1] != "'":
            lexeme += self.next_char()
        self.pos += 1
        return lexeme

    def read_keyword(self):
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isalnum() or self.text[self.pos + 1] == '_' :
            lexeme += self.next_char()
        lexeme.lower() # pascal nije case sensitive
        if lexeme == 'if':
            return Token(Class.IF, lexeme)
        elif lexeme == 'else':
            return Token(Class.ELSE, lexeme)
        elif lexeme == 'while':
            return Token(Class.WHILE, lexeme)
        elif lexeme == 'for':
            return Token(Class.FOR, lexeme)
        elif lexeme == 'break':
            return Token(Class.BREAK, lexeme)
        elif lexeme == 'repeat':
            return Token(Class.REPEAT, lexeme)
        elif lexeme == 'until':
            return Token(Class.UNTIL, lexeme)
        elif lexeme == 'continue':
            return Token(Class.CONTINUE, lexeme)
        elif lexeme == 'integer' or lexeme == 'char' or lexeme == 'string' or lexeme == 'real' or lexeme == 'boolean':
            return Token(Class.TYPE, lexeme)
        elif lexeme == 'begin':
            return Token(Class.BEGIN, lexeme)
        elif lexeme == 'end':
            return Token(Class.END, lexeme)
        elif lexeme == 'var':
            return Token(Class.VAR, lexeme)
        elif lexeme == 'and':
            return Token(Class.AND, lexeme)
        elif lexeme == 'or':
            return Token(Class.OR, lexeme)
        elif lexeme == 'not':
            return Token(Class.NOT, lexeme)
        elif lexeme == 'xor':
            return Token(Class.XOR, lexeme)
        elif lexeme == 'function':
            return Token(Class.FUNCTION, lexeme)
        elif lexeme == 'procedure':
            return Token(Class.PROCEDURE, lexeme)
        elif lexeme == 'array':
            return Token(Class.ARRAY, lexeme)
        elif lexeme == 'of':
            return Token(Class.OF, lexeme)
        elif lexeme == 'do':
            return Token(Class.DO, lexeme)
        elif lexeme == 'to':
            return Token(Class.TO, lexeme)
        elif lexeme == 'downto':
            return Token(Class.DOWNTO, lexeme)    
        elif lexeme == 'then':
            return Token(Class.THEN, lexeme)
        elif lexeme == 'true' or lexeme == 'false':
            return Token(Class.BOOLEAN, lexeme)
        elif lexeme == 'div':
            return Token(Class.DIV, lexeme)
        elif lexeme == 'mod':
            return Token(Class.MOD, lexeme)
        elif lexeme == 'exit':
            return Token(Class.EXIT, lexeme)
        return Token(Class.ID, lexeme)

    def next_char(self):
        self.pos += 1
        if self.pos >= self.len:
            return None
        return self.text[self.pos]

    def next_token(self):
        self.read_space()
        curr = self.next_char()
        if curr is None:
            return Token(Class.EOF, curr) 
        token = None
        if curr.isalpha():
            token = self.read_keyword()
        elif curr.isdigit():
            number = self.read_int()
            if '.' not in number:
                token = Token(Class.INTEGER, number)
            else:
                token = Token(Class.REAL, number)
        elif curr == '\'':
            curr = self.next_char()
            curr = self.next_char()
            if curr == '\'':
                self.pos -= 2
                token = Token(Class.CHAR, self.read_char())
            else:
                self.pos -= 2
                token = Token(Class.STRING, self.read_string())
        elif curr == '+':
            token = Token(Class.PLUS, curr)
        elif curr == '-':
            token = Token(Class.MINUS, curr)
        elif curr == '*':
            token = Token(Class.STAR, curr)
        elif curr == '/':
            token = Token(Class.FWDSLASH, curr)
        elif curr == '=':
            token = Token(Class.EQ, '=')
        elif curr == ':':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.ASSIGN, ':=')
            else:
                token = Token(Class.DECL, ':')
                self.pos -= 1
        elif curr == '<':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.LTE, '<=')
            elif curr == '>':
                token = Token(Class.NEQ, '<>')
            else:
                token = Token(Class.LT, '<')
                self.pos -= 1
        elif curr == '>':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.GTE, '>=')
            else:
                token = Token(Class.GT, '>')
                self.pos -= 1
        elif curr == '(':
            token = Token(Class.LPAREN, curr)
        elif curr == ')':
            token = Token(Class.RPAREN, curr)
        elif curr == '[':
            token = Token(Class.LBRACKET, curr)
        elif curr == ']':
            token = Token(Class.RBRACKET, curr)
        elif curr == ';':
            token = Token(Class.SEMICOLON, curr)
        elif curr == '.':
            curr = self.next_char()
            if curr == '.':
                token = Token(Class.TWODOTS, '..')
            else:
                token = Token(Class.DOT, '.')
                self.pos -= 1
        elif curr == ',':
            token = Token(Class.COMMA, curr)
        else:
            self.die(curr)
        return token

    def lex(self):
        tokens = []
        while True:
            curr = self.next_token()
            tokens.append(curr)
            if curr.class_ == Class.EOF:
                break
        return tokens

    def die(self, char):
        raise SystemExit("Unexpected character: {}".format(char))