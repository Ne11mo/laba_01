from constans import AVAILABLE_SYMBOLS, INVALID_COMBINATIONS, BINARY_OPERATORS
from src.toolkit.errors import (
    CalculatorErrors,
    InvalidExpressionError,
    InvalidCharacterError,
    BracketsError,
    EmptyExpressionError,
    UnaryOperatorError
)

def validate_expression(expression):
    expression = expression.strip().replace(' ', '')

    if expression == '':
        raise EmptyExpressionError

    brackets = 0
    for symbol in expression:
        if symbol == '(':
            brackets += 1
        elif symbol == ')':
            brackets -= 1
            if brackets < 0:
                raise BracketsError("Закрывающая скобка без открывающей")
        elif symbol not in AVAILABLE_SYMBOLS:
            raise InvalidCharacterError("В выражении есть недопустимый символ")

    for i in INVALID_COMBINATIONS:
        if i in expression:
            raise InvalidExpressionError("В выражении есть два бинарных операнда подряд")


def tokenization(expression):
    tokens = []
    expression = expression.strip().replace(' ', '')
    expression = expression.replace('//', '!') # распознавание целочисленного деления

    current_num = ''
    for symbol in expression:
        if symbol not in '0123456789.,':
            if current_num != '':
                tokens.append(current_num)
                current_num = ''
            tokens.append(symbol)
        else:
            current_num += symbol
    if current_num != '':
        tokens.append(current_num)

    return recognize_unary_operators(tokens)


def recognize_unary_operators(tokens):
    final_tokens = []
    count_minus = 0
    is_series = False

    for token in tokens:
        is_need_to_simplify = is_series or len(final_tokens) == 0 or final_tokens[-1] in BINARY_OPERATORS or final_tokens[-1] == '('
        if (token == '+' or token == '-') and is_need_to_simplify:
            is_series = True
            if token == '-':
                count_minus += 1
            continue

        if is_series:
            final_tokens.append('$' if count_minus % 2 == 1 else '@')
            is_series = False
            count_minus = 0
        final_tokens.append(token)

    if is_series:
        raise UnaryOperatorError("Неправильно расставлены унарные знаки")

    return final_tokens


def start_calculator(expression):
    try:
        validate_expression(expression)
        tokens = tokenization(expression)

        postfix_expression = convert_to_postfix_notation(tokens)
        result = calculate(postfix_expression)

        print(f'Результат: {result}')
    # различные ошибки, выбрасываемые программой (доделать)
    except CalculatorErrors as e:
        print(f'Ошибка: {e}')