from .validation import validate_expression
from .tokenization import tokenization

def start_calculator(expression):
    try:
        tokens = tokenization(expression)
        validate_expression(tokens, expression)

        postfix_expression = convert_to_postfix_notation(tokens)
        result = calculate(postfix_expression)

        print(f'Результат: {result}')
    # различные ошибки, выбрасываемые программой (доделать)
    except CalculatorErrors as e:
        print(f'Ошибка: {e}')