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


class EmptyExpressionError(CalculatorErrors):
    pass


class EmptyOperationError(CalculatorErrors):
    pass


class DoubleBinaryOperationError(CalculatorErrors):
    pass


class InvalidNumberError(CalculatorErrors):
    pass


class ConverterErrors(Exception):
    """Базовая ошибка конвертера"""


class InvalidUnitError(ConverterErrors):
    pass


class DifferentUnitsError(ConverterErrors):
    pass


class UnderAbsoluteZeroTemperatureError(ConverterErrors):
    pass
