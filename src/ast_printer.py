from src.expr import Visitor

class AST_Printer(Visitor):
    def print(self, expr):
        return expr.accept(self)
    
    def visit_binary_expr