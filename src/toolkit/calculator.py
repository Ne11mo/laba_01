from constans import AVAILABLE_SYMBOLS, INVALID_COMBINATIONS, BINARY_OPERATORS, UNARY_OPERATORS
from src.toolkit.errors import (
    CalculatorErrors,
    InvalidExpressionError,
    InvalidCharacterError,
    BracketsError,
    EmptyExpressionError,
    UnaryOperatorError,
    EmptyOperandError,
    DoubleBinaryOperandError
)

def is_number(token):
    if token[0] in '0123456789':
        return True
    return False

def tokenization(expression):
    tokens = []
    expression = expression.strip()
    expression = expression.replace('//', '!') # распознавание целочисленного деления

    current_num = ''
    for symbol in expression:
        if symbol not in '0123456789.,':
            if current_num != '':
                tokens.append(current_num)
                current_num = ''
            if symbol != ' ':
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

    return final_tokens


def validate_expression(tokens):
    if len(tokens) == 0:
        raise EmptyExpressionError("Пустая строка")
    if len(tokens) == 1:
        raise InvalidExpressionError("Некорректное выражение")

    brackets = 0
    for index_token in range(len(tokens)):
        if tokens[index_token] == '(':
            brackets += 1
        elif tokens[index_token] == ')':
            brackets -= 1
            if brackets < 0:
                raise BracketsError("Закрывающая скобка без открывающей")

        if tokens[index_token] not in AVAILABLE_SYMBOLS:
            raise InvalidCharacterError("В выражении есть недопустимый символ")

        if index_token != 0:
            if is_number(tokens[index_token - 1]) and is_number(tokens[index_token]):
                raise EmptyOperandError("Пропущен операнд")
            if tokens[index_token-1] in BINARY_OPERATORS and tokens[index_token] in BINARY_OPERATORS:
                raise DoubleBinaryOperandError("Два бинарных операнда подряд")
            if (tokens[index_token - 1] in BINARY_OPERATORS or tokens[index_token] in UNARY_OPERATORS) and tokens[index_token] == ')':
                raise InvalidExpressionError("Неправильно расставлены операнды")

    if tokens[-1] in BINARY_OPERATORS or tokens[-1] in UNARY_OPERATORS:
        raise InvalidExpressionError("Неправильно расставлены операнды")


def start_calculator(expression):
    try:
        tokens = tokenization(expression)
        validate_expression(tokens)

        postfix_expression = convert_to_postfix_notation(tokens)
        result = calculate(postfix_expression)

        print(f'Результат: {result}')
    # различные ошибки, выбрасываемые программой (доделать)
    except CalculatorErrors as e:
        print(f'Ошибка: {e}')