class Lox_Error:

    had_error = False

    def error(line, message):
        Lox_Error.report(line, "", message)
    
    def report(line, where, message):
        print(f"[line {line} Error {where}: {message}]")
        Lox_Error.had_error = True