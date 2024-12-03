from src.token_type import Token_Type

class Lox_Error:

    had_error = False

    def error(line, message):
        Lox_Error.report(line, "", message)
    
    def report(line, where, message):
        print(f"[line {line} Error {where}: {message}]")
        Lox_Error.had_error = True

    def parse_error(token, message):
        if token.type == Token_Type.EOF:
            Lox_Error.report(token.line, " at end", message)
        else:
            Lox_Error.report(token.line, f" at '{token.lexeme}'", message)