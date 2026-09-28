class CalculatorErrors(Exception):
    """Базовая ошибка калькулятора"""

class InvalidExpressionError(CalculatorErrors):
    pass

class BracketsError(CalculatorErrors):
    pass

class InvalidCharacterError(CalculatorErrors):
    pass

class DivisionByZeroError(CalculatorErrors):
    pass