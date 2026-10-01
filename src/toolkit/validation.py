from .constants import AVAILABLE_SYMBOLS, BINARY_OPERATORS, UNARY_OPERATORS
from .errors import (
    BracketsError,
    DoubleBinaryOperationError,
    EmptyExpressionError,
    EmptyOperationError,
    InvalidCharacterError,
    InvalidExpressionError,
    InvalidNumberError,
)


def is_number(token):
    return bool(token != "" and token[0].isdigit())


def check_on_invalid_symbols(expression):
    for symbol in expression:
        if symbol not in AVAILABLE_SYMBOLS and symbol != " ":
            raise InvalidCharacterError(" В выражении присутствует недопустимый символ")


def check_on_invalid_number(token):
    if token == "":
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token[0] == ".":
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token.count(".") > 1:
        raise InvalidNumberError("В выражении есть неправильная запись числа")
    if token[-1] == ".":
        raise InvalidNumberError("В выражении есть неправильная запись числа")

    return True


def validate_expression(tokens, expression):
    if len(tokens) == 0:
        raise EmptyExpressionError("Пустая строка")

    check_on_invalid_symbols(expression)

    brackets = 0
    expect_operand = True  # ожидание операнда

    for index_token in range(len(tokens)):
        if tokens[index_token] in BINARY_OPERATORS:
            if expect_operand:
                if index_token != 0 and tokens[index_token - 1] in BINARY_OPERATORS:
                    raise DoubleBinaryOperationError("Два бинарных оператора подряд")

                raise InvalidExpressionError("Неправильно расставлены операнды")

            expect_operand = True

        elif tokens[index_token] in UNARY_OPERATORS:
            if not expect_operand:
                raise InvalidExpressionError("Неправильно расставлены операнды")
            expect_operand = True

        elif tokens[index_token] == "(":
            if not expect_operand:
                raise InvalidExpressionError("Пропущен бинарный оператор")

            brackets += 1
            expect_operand = True

        elif tokens[index_token] == ")":
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
                    raise EmptyOperationError("Пропущен операнд")
                raise InvalidExpressionError("Пропущен бинарный оператор")

            expect_operand = False

    if brackets != 0:
        raise BracketsError("Неверно расставлены скобки")

    if expect_operand:
        raise InvalidExpressionError("Неправильно расставлены операнды")
