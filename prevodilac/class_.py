from enum import Enum, auto


class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    FWDSLASH = auto()
    MOD = auto()
    DIV = auto()

    OR = auto()
    AND = auto()
    NOT = auto()
    XOR = auto()

    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()

    VAR = auto()
    BEGIN = auto()
    END = auto()
    FUNCTION = auto()
    PROCEDURE = auto()
    EXIT = auto()

    ASSIGN = auto()
    DECL = auto()
    SEMICOLON = auto()
    COMMA = auto()

    TYPE = auto()
    INTEGER = auto()
    CHAR = auto()
    STRING = auto()
    REAL = auto()
    BOOLEAN = auto()
    
    TRUE = auto()
    FALSE = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    REPEAT = auto()
    UNTIL = auto()
    

    DO = auto()
    TO = auto()
    DOWNTO = auto()
    THEN = auto()

    ARRAY = auto()
    OF = auto()
    TWODOTS = auto()
    DOT = auto()

    BREAK = auto()
    CONTINUE = auto()
   # RETURN = auto()

   # ADDRESS = auto()

    ID = auto()
    EOF = auto()
