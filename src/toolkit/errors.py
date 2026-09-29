class CalculatorErrors(Exception):
    """Базовая ошибка калькулятора"""

class InvalidExpressionError(CalculatorErrors):
    pass

class BracketsError(CalculatorErrors):
    pass

class InvalidCharacterError(CalculatorErrors):
    pass

class UnaryOperatorError(CalculatorErrors):
    pass

class DivisionByZeroError(CalculatorErrors):
    pass

class EmptyExpressionError(CalculatorErrors):
    pass

class EmptyOperandError(CalculatorErrors):
    pass

class DoubleBinaryOperandError(CalculatorErrors):
    pass