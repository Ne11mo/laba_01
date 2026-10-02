from decimal import ROUND_HALF_UP, Decimal, getcontext

from .constants import UNARY_OPERATORS
from .errors import DivisionByZeroError
from .tokenization import tokenization
from .validation import is_number, validate_expression

getcontext().prec = 28  # установка точности


def rating_operation(operation: str) -> int:
    if operation in "+-":
        return 0
    elif operation in "*/!%":
        return 1
    elif operation in "@$":
        return 2
    return -1


def do_binary_operation(
    first_number: Decimal, second_number: Decimal, operation: str
) -> Decimal:
    if operation == "+":
        return first_number + second_number
    elif operation == "-":
        return first_number - second_number
    elif operation == "*":
        return first_number * second_number
    elif operation == "/":
        if second_number == Decimal("0"):
            raise DivisionByZeroError("Деление на ноль")
        return first_number / second_number
    elif operation == "%":
        return first_number % second_number
    elif operation == "!":
        return first_number // second_number


def do_unary_operation(number: Decimal, operation: str) -> Decimal:
    if operation == "$":
        return Decimal("-1") * number
    return number


def convert_to_postfix_notation(tokens: list) -> list:
    postfix_notation = []
    stack_for_convert = ["("]

    tokens.append(")")

    for token in tokens:
        if is_number(token):
            postfix_notation.append(Decimal(token))
        elif token == ")":
            while stack_for_convert[-1] != "(":
                postfix_notation.append(stack_for_convert[-1])
                stack_for_convert.pop()
            stack_for_convert.pop()
        elif token == "(":
            stack_for_convert.append(token)
        else:
            while rating_operation(stack_for_convert[-1]) >= rating_operation(token):
                postfix_notation.append(stack_for_convert[-1])
                stack_for_convert.pop()

            stack_for_convert.append(token)

    return postfix_notation


def calculate(postfix_notation: list) -> Decimal:
    stack_for_calculate = []
    for token in postfix_notation:
        if isinstance(token, Decimal):
            stack_for_calculate.append(token)
        else:
            if token in UNARY_OPERATORS:
                number = stack_for_calculate[-1]
                stack_for_calculate.pop()

                result = do_unary_operation(number, token)
                stack_for_calculate.append(result)
            else:
                second_number = stack_for_calculate[-1]
                stack_for_calculate.pop()
                first_number = stack_for_calculate[-1]
                stack_for_calculate.pop()

                result = do_binary_operation(first_number, second_number, token)
                stack_for_calculate.append(result)

    result = (
        stack_for_calculate[0]
        .quantize(Decimal("0.0000000001"), ROUND_HALF_UP)
        .normalize()
    )
    return result


def start_calculator(expression: str) -> Decimal:
    tokens = tokenization(expression)
    validate_expression(tokens, expression)

    postfix_expression = convert_to_postfix_notation(tokens)
    result = calculate(postfix_expression)

    return result
