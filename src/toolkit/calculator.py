from .constans import UNARY_OPERATORS
from .errors import CalculatorErrors, DivisionByZeroError
from .tokenization import tokenization
from .validation import is_number, validate_expression


def rating_operation(operation):
    if operation in "+-":
        return 0
    elif operation in "*/!%":
        return 1
    elif operation in "@$":
        return 2
    return -1


def do_binary_operation(first_number, second_number, operation):
    if operation == "+":
        return first_number + second_number
    elif operation == "-":
        return first_number - second_number
    elif operation == "*":
        return first_number * second_number
    elif operation == "/":
        if second_number == 0:
            raise DivisionByZeroError("Деление на ноль")
        return first_number / second_number
    elif operation == "%":
        return first_number % second_number
    elif operation == "!":
        return first_number // second_number


def do_unary_operation(number, operation):
    if operation == "$":
        return -number
    return number


def convert_to_postfix_notation(tokens):
    postfix_notation = []
    stack_for_convert = ["("]

    tokens.append(")")

    for token in tokens:
        if is_number(token):
            postfix_notation.append(float(token))
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


def calculate(postfix_notation):
    stack_for_calculate = []
    for token in postfix_notation:
        if is_number(str(token)):
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

    return stack_for_calculate[0]


def start_calculator(expression):
    try:
        tokens = tokenization(expression)
        validate_expression(tokens, expression)

        postfix_expression = convert_to_postfix_notation(tokens)
        result = calculate(postfix_expression)

        return result
    # различные ошибки, выбрасываемые калькулятором
    except CalculatorErrors as e:
        return e
