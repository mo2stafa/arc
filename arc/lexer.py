from collections import deque
from tokens import *

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1
        self.buffer = deque()


    def advance(self):
        if self.current_char == "\n":
            self.line += 1
            self.column = 0

        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None

        else:
            self.current_char = self.text[self.pos]
            self.column += 1


    def peek(self):
        if self.pos + 1 > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos + 1]


    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()


    def skip_single_comment(self):
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()


    def skip_multi_comment(self):
        while self.current_char is not None and (self.current_char != "*" or self.peek() != "/"):
            self.advance()
        self.advance()
        self.advance()


    def get_number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            return Token(TokenType.FLOATL, float(result), line=self.line, column=self.column)
        else:
            return Token(TokenType.INTL, int(result), line=self.line, column=self.column)
        

    def get_variable(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        if result in RESERVED_KEYWORDS:
            return Token(RESERVED_KEYWORDS[result], result, line=self.line, column=self.column)

        return Token(TokenType.TYPE, result, line=self.line, column=self.column)
    

    def get_string(self):
        self.advance()

        result = ""
        while self.current_char is not None and self.current_char != "\"":
            result += self.current_char
            self.advance()

        if self.current_char == "\"":
            self.advance()

        return Token(TokenType.STRINGL, result, line=self.line, column=self.column)


    def get_next_symbol(self):
        if self.peek() is not None:
            s = self.current_char + self.peek()

            if s in SYMBOLS:
                self.advance()
                self.advance()
                return Token(SYMBOLS[s], s, line=self.line, column=self.column)

        s = self.current_char
        if s in SYMBOLS:
            self.advance()
            return Token(SYMBOLS[s], s, line=self.line, column=self.column)
        

    def load_next_token_into_buffer(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()

            elif self.current_char == "/" and self.peek() == "/":
                self.skip_single_comment()

            elif self.current_char == "/" and self.peek() == "*":
                self.skip_multi_comment()

            elif self.current_char == "\"":
                self.buffer.append(self.get_string())

            elif self.current_char.isdigit():
                self.buffer.append(self.get_number())

            elif self.current_char.isalpha() or self.current_char == "_":
                self.buffer.append(self.get_variable())

            else:
                self.buffer.append(self.get_next_symbol())

        self.buffer.append(Token(TokenType.EOF, None, line=self.line, column=self.column))


    def get_next_token(self):
        if len(self.buffer) == 0:
            self.load_next_token_into_buffer()
        return self.buffer.popleft()


    def peek_nth_next_token(self, n):
        while len(self.buffer) == 0 or (len(self.buffer) <= n and self.buffer[-1].type != TokenType.EOF):
            self.load_next_token_into_buffer()
        if n < len(self.buffer):
            return self.buffer[n]
        return self.buffer[-1]