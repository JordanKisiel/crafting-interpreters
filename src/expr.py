from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor):
        self.visitor = visitor

class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(expr):
        pass

    @abstractmethod
    def visit_grouping_expr(expr):
        pass

    @abstractmethod
    def visit_literal_expr(expr):
        pass

    @abstractmethod
    def visit_unary_expr(expr):
        pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
       return visitor.visit_binary_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
       return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
       return visitor.visit_literal_expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
       return visitor.visit_unary_expr(self)

