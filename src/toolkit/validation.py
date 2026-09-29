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
    if token != '' and token[0].isdigit():
        return True
    return False


def check_on_invalid_symbols(expression):
    for symbol in expression:
        if symbol not in AVAILABLE_SYMBOLS and symbol != ' ':
            raise InvalidCharacterError(" В выражении присутствует недопустимый символ")


def check_on_invalid_number(token):
    if token == '':
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token[0] == ',' or token[0] == '.':
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token.count(',') + token.count('.') > 1:
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token[-1] == ',' or token[-1] == '.':
        raise InvalidNumberError("В выражении есть неправильная запись числа")

    return True


def validate_expression(tokens, expression):
    if len(tokens) == 0:
        raise EmptyExpressionError("Пустая строка")

    check_on_invalid_symbols(expression)

    brackets = 0
    expect_operand = True #ожидание операнда

    for index_token in range(len(tokens)):
        if tokens[index_token] in BINARY_OPERATORS:
            if expect_operand:
                if index_token != 0 and tokens[index_token - 1] in BINARY_OPERATORS:
                    raise DoubleBinaryOperandError("Два бинарных оператора подряд")

                raise InvalidExpressionError("Неправильно расставлены операнды")

            expect_operand = True

        elif tokens[index_token] in UNARY_OPERATORS:
            if not expect_operand:
                raise InvalidExpressionError("Неправильно расставлены операнды")
            expect_operand = True

        elif tokens[index_token] == '(':
            if not expect_operand:
                raise InvalidExpressionError("Пропущен бинарный оператор")
            if index_token != 0 and tokens[index_token - 1] in UNARY_OPERATORS:
                raise InvalidExpressionError("ошибка в выражении")

            brackets += 1
            expect_operand = True

        elif tokens[index_token] == ')':
            brackets -= 1
            if brackets < 0:
                raise BracketsError("Нельзя закрывающую скобку без открывающей")
            if expect_operand:
                raise InvalidExpressionError("Неправильно расставлены операнды")

            expect_operand = False

        else:
            check_on_invalid_number(tokens[index_token])

            if not expect_operand:
                if index_token != 0 and is_number(tokens[index_token - 1]):
                    raise EmptyOperandError("Пропущен операнд")
                raise InvalidExpressionError("Пропущен бинарный оператор")

            expect_operand = False



    if brackets != 0:
        raise BracketsError("Неверно расставлены скобки")

    if expect_operand:
        raise InvalidExpressionError("Неправильно расставлены операнды")
