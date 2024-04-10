import sys
from lexer import Lexer
from tokens import TokenType

def main():
    if len(sys.argv) <= 1:
        raise FileNotFoundError("No arc file provided")
    
    file = open(sys.argv[1], "r")
    code = file.read()

    lexer = Lexer(code)
    while True:
        token = lexer.get_next_token()
        print(f'({token.value} , {token.type})')
        if token.type == TokenType.EOF:
            break



if __name__ == "__main__":
    main()