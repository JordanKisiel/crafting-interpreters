class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return f"Token(type:{self.type}, lexeme: {self.lexeme}, literal: {self.literal})"
        