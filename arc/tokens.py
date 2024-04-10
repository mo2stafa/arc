from enum import Enum

class Token(object):
    def __init__(self, token_type, value, line = -1, column = -1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column




class TokenType(Enum):
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    ASSIGN = "="
    LRPAR = "("
    RRPAR = ")"
    LCPAR = "{"
    RCPAR = "}"
    SEMI = ";"
    INT = "int"
    FLOAT = "float"
    RETURN = "return"

    EOF = "EOF"
    TYPE = "TYPE"
    INTL = "INTL"
    FLOATL = "FLOATL"
    STRINGL = "STRINGL"




SYMBOLS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "=": TokenType.ASSIGN,
    "(": TokenType.LRPAR,
    ")": TokenType.RRPAR,
    "{": TokenType.LCPAR,
    "}": TokenType.RCPAR,
    ";": TokenType.SEMI,
}

RESERVED_KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "return": TokenType.RETURN
}