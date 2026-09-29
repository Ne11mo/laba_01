HELP_MESSAGE = """\
 -Input \"mode\" for selecting the mode or to exit the current mode and select the new mode
 -Input the string for calculation, following the input rules for different modes
 -Input \"help\" to view the work navigation
 -Input \"stop\" to stop the program
"""

AVAILABLE_SYMBOLS = ['+', '-', '*', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%', '.', ',', '@', '$']
INVALID_COMBINATIONS = []
for i in '+-*%.,/':
    for j in '*%.,/':
        if i + j != '//':
            INVALID_COMBINATIONS.append(i + j)
INVALID_COMBINATIONS.append('///')
INVALID_COMBINATIONS.append('.+')
INVALID_COMBINATIONS.append(',+')
INVALID_COMBINATIONS.append('.-')
INVALID_COMBINATIONS.append(',-')

UNARY_OPERATORS = ['@', '$']
BINARY_OPERATORS = ['+', '-', '*', '/']