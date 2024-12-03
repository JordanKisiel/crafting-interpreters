from src.expr import *
from src.token import Token
from src.token_type import Token_Type
from src.ast_printer import AST_Printer

def main():
    expression = Binary(
        Unary(
            Token(Token_Type.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(Token_Type.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    ast_printer = AST_Printer()
    print(ast_printer.print(expression))


main()