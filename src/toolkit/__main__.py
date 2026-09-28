import argparse
from src.toolkit.calculator import start_calculator


def create_parsers():
    parser = argparse.ArgumentParser(prog="python -m toolkit", description="toolkit") # создание главного парсера
    subparser = parser.add_subparsers(dest='command', required=True, help="Набор команд") # создание группы для подкоманд

    # создание парсера для калькулятора
    parser_calculator = subparser.add_parser('calc', help="Вычисление математических выражений")
    parser_calculator.add_argument('expression', type=str, help="Выражение записывается в кавычках")

    # создание парсера для конвертера
    parser_converter = subparser.add_parser('convert', help="Конвертация величин")
    parser_converter.add_argument('value', type=float, help="Исходное значение для конвертации")
    parser_converter.add_argument('--from', dest='unit_from', type=str, help="Исходная единица")
    parser_converter.add_argument('--to', dest='unit_to', type=str, help="Конечная единица")

    return parser, subparser, parser_calculator, parser_converter


def main():
    parser, subparser, parser_calculator, parser_converter = create_parsers()
    args = parser.parse_args()

    if args.command == 'calc':
        start_calculator(args.expression) # запуск калькулятора

    elif args.command == 'convert':
        start_converter() # запуск конвертера


if __name__ == '__main__':
    main()