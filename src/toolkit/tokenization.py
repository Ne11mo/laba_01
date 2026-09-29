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
