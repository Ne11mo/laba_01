from .constans import AVAILABLE_SYMBOLS, BINARY_OPERATORS, UNARY_OPERATORS
from .errors import (
    InvalidExpressionError,
    InvalidCharacterError,
    BracketsError,
    EmptyExpressionError,
    EmptyOperandError,
    DoubleBinaryOperandError,
    InvalidNumberError
)

def is_number(token):
    if token[0] in '0123456789':
        return True
    return False


def check_on_invalid_symbols(expression):
    for symbol in expression:
        if symbol not in AVAILABLE_SYMBOLS and symbol != ' ':
            raise InvalidCharacterError(" В выражении присутствует недопустимый символ")


def check_on_invalid_number(token):
    if token[0] == ',' or token[0] == '.':
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token.count(',') + token.count('.') > 1:
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token[-1] == ',' or token[-1] == '.':
        raise InvalidNumberError("В выражении есть неправильная запись числа")

    for index_digit in range(len(token)):
        if token[index_digit] == '.' or token[index_digit] == ',':
            if token[index_digit-1] in '0123456789.,' and token[index_digit+1] in '0123456789.,':
                raise InvalidNumberError("В выражении есть неправильная запись числа")

    return True


def validate_expression(tokens, expression):
    if len(tokens) == 0:
        raise EmptyExpressionError("Пустая строка")
    if len(tokens) == 1 and check_on_invalid_number(tokens[0]):
        raise InvalidExpressionError("Некорректное выражение")

    check_on_invalid_symbols(expression)

    brackets = 0
    for index_token in range(len(tokens)):
        if tokens[index_token] == '(':
            brackets += 1
        elif tokens[index_token] == ')':
            brackets -= 1
            if brackets < 0:
                raise BracketsError("Закрывающая скобка без открывающей")

        if tokens[index_token] not in BINARY_OPERATORS and tokens[index_token] not in UNARY_OPERATORS and tokens[index_token] not in ')(':
            check_on_invalid_number(tokens[index_token])

        if index_token != 0:
            if is_number(tokens[index_token - 1]) and is_number(tokens[index_token]):
                raise EmptyOperandError("Пропущен операнд")
            if tokens[index_token-1] in BINARY_OPERATORS and tokens[index_token] in BINARY_OPERATORS:
                raise DoubleBinaryOperandError("Два бинарных операнда подряд")
            if (tokens[index_token - 1] in BINARY_OPERATORS or tokens[index_token - 1] in UNARY_OPERATORS) and tokens[index_token] == ')':
                raise InvalidExpressionError("Неправильно расставлены операнды")

    if brackets != 0:
        raise BracketsError("Неверно расставлены скобки")

    if tokens[-1] in BINARY_OPERATORS or tokens[-1] in UNARY_OPERATORS:
        raise InvalidExpressionError("Неправильно расставлены операнды")
