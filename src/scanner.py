from src.token import Token
from src.token_type import Token_Type
from src.lox_error import Lox_Error

class Scanner:

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            # beginning of the next lexeme
            self.start = self.current
            self.scan_token()

        # add eof token at end of token list
        self.tokens.append(Token(Token_Type.EOF, "", None, self.line))
        return self.tokens
    
    def scan_token(self):
        char = self.advance()

        match char:
            case '(': self.add_token(Token_Type.LEFT_PAREN)
            case ')': self.add_token(Token_Type.RIGHT_PAREN)
            case '{': self.add_token(Token_Type.LEFT_BRACE)
            case '}': self.add_token(Token_Type.RIGHT_BRACE)
            case ',': self.add_token(Token_Type.COMMA)
            case '.': self.add_token(Token_Type.DOT)
            case '-': self.add_token(Token_Type.MINUS)
            case '+': self.add_token(Token_Type.PLUS)
            case ';': self.add_token(Token_Type.SEMICOLON)
            case '*': self.add_token(Token_Type.STAR)

            case '!':
                self.add_token(Token_Type.BANG_EQUAL if self.match("=") else Token_Type.BANG)
            case '=':
                self.add_token(Token_Type.EQUAL_EQUAL if self.match("=") else Token_Type.EQUAL)
            case '<':
                self.add_token(Token_Type.LESS_EQUAL if self.match("=") else Token_Type.LESS)
            case '>':
                self.add_token(Token_Type.GREATER_EQUAL if self.match("=") else Token_Type.GREATER)

            case '/':
                if self.match("/"):
                    # comment goes until the end of the line
                    # ignore comments
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(Token_Type.SLASH)

            # ignore white space 
            case ' ' | '\r' | '\t':
                pass

            case '\n':
                self.line += 1
            

            #default
            case _:
                Lox_Error.error(self.line, "Unexpected character.")

    
    def is_at_end(self):
        return self.current >= len(self.source)
    
    def advance(self):
        current_char = self.source[self.current]
        self.current += 1
        return current_char 
    
    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True
    
    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    
    def add_token(self, type, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    
