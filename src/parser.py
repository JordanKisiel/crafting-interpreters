from src.token_type import Token_Type
from src.expr import *
from src.lox_error import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except Parse_Error:
            return None

    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()

        while self.match([Token_Type.BANG_EQUAL, Token_Type.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr
    
    def comparison(self):
        expr = self.term()

        while self.match([Token_Type.GREATER, 
                         Token_Type.GREATER_EQUAL, 
                         Token_Type.LESS, 
                         Token_Type.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr
    
    def term(self):
        expr = self.factor()

        while self.match([Token_Type.MINUS, Token_Type.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def factor(self):
        expr = self.unary()

        while self.match([Token_Type.SLASH, Token_Type.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr
    
    def unary(self):
        if self.match([Token_Type.BANG, Token_Type.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if self.match([Token_Type.FALSE]):
            return Literal(False)
        if self.match([Token_Type.TRUE]):
            return Literal(True)
        if self.match([Token_Type.NIL]):
            return Literal(None)
        
        if self.match([Token_Type.NUMBER, Token_Type.STRING]):
            return Literal(self.previous().literal)
        
        if self.match([Token_Type.LEFT_PAREN]):
            expr = self.expression()
            self.consume(Token_Type.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")

    # helper methods ----------------------------------------------------------------- 
    def match(self, token_types):
        for type in token_types:
            if self.check(type):
                self.advance()
                return True
        
        return False 
    
    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return self.peek().type == Token_Type.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        
        raise self.error(self.peek(), message) 

    def error(self, token, message):
        Lox_Error.parse_error(token, message)
        return Parse_Error()
    
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == Token_Type.SEMICOLON:
                return

            match self.peek().type:
                case (Token_Type.CLASS | 
                      Token_Type.FUN | 
                      Token_Type.VAR | 
                      Token_Type.FOR | 
                      Token_Type.IF | 
                      Token_Type.WHILE | 
                      Token_Type.PRINT | 
                      Token_Type.RETURN):
                    return
            
            self.advance()


class Parse_Error(RuntimeError):
    def __init__(self):
        super().__init__()
