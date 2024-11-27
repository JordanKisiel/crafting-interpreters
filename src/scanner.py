from src.token import Token
from src.token_type import Token_Type
from src.lox_error import Lox_Error

class Scanner:

    keywords = {
        "and": Token_Type.AND,
        "class": Token_Type.CLASS,
        "else": Token_Type.ELSE,
        "false": Token_Type.FALSE,
        "for": Token_Type.FOR,
        "fun": Token_Type.FUN,
        "if": Token_Type.IF,
        "nil": Token_Type.NIL,
        "or": Token_Type.OR,
        "print": Token_Type.PRINT,
        "return": Token_Type.RETURN,
        "super": Token_Type.SUPER,
        "this": Token_Type.THIS,
        "true": Token_Type.TRUE,
        "var": Token_Type.VAR,
        "while": Token_Type.WHILE
    }

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

            # string literal
            case '"': 
                self.add_string()

            #default
            case _:
                if self.is_digit(char):
                    self.add_number()
                elif self.is_alpha(char):
                    self.add_identifier()
                else:
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

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    
    def add_token(self, type, literal = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    
    def add_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            Lox_Error.error(self.line, "Unterminated string.")
            return
        
        # closing "
        self.advance()

        # trim off the quote marks
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(Token_Type.STRING, value)

    def add_number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # look for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # consume '.'
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()
        
        self.add_token(Token_Type.NUMBER, float(self.source[self.start : self.current]))

    def add_identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        type = None
        if text in Scanner.keywords:
            type = Scanner.keywords[text]
        if type == None:
            type = Token_Type.IDENTIFIER

        self.add_token(type)

    def is_digit(self, char):
        return char >= '0' and char <= '9'

    def is_alpha(self, char):
        is_lowercase = char >= 'a' and char <= 'z'
        is_uppercase = char >= 'A' and char <= 'Z'
        is_underscore = char == '_'
        return is_lowercase or is_uppercase or is_underscore

    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)