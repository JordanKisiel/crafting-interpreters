from src.expr import Visitor

class AST_Printer(Visitor):
    def print(self, expr):
        return expr.accept(self)
    
    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", [expr.expression])

    def visit_literal_expr(self, expr):
        if expr.value == None:
            return "nil" 
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, [expr.right]) 

    def parenthesize(self, name, exprs):
        str = f"({name}"

        for expr in exprs:
            str += " "
            str += expr.accept(self)
        
        str += ")"

        return str
