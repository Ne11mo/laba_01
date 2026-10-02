import argparse
import sys

from .calculator import start_calculator
from .converter import start_converter
from .errors import CalculatorErrors, ConverterErrors
from .history import (
    save_history_of_successful_calculation,
    save_history_of_successful_conversion,
)


def create_parsers():
    parser = argparse.ArgumentParser(
        prog="python -m toolkit", description="toolkit"
    )  # создание главного парсера
    subparser = parser.add_subparsers(
        dest="command", required=True, help="Набор команд"
    )  # создание группы для подкоманд

    # создание парсера для калькулятора
    parser_calculator = subparser.add_parser(
        "calc", help="Вычисление математических выражений"
    )
    parser_calculator.add_argument(
        "expression", type=str, help="Выражение записывается в кавычках"
    )

    # создание парсера для конвертера
    parser_converter = subparser.add_parser("convert", help="Конвертация величин")
    parser_converter.add_argument(
        "value", type=float, help="Исходное значение для конвертации"
    )
    parser_converter.add_argument(
        "--from", dest="unit_from", type=str, help="Исходная единица"
    )
    parser_converter.add_argument(
        "--to", dest="unit_to", type=str, help="Конечная единица"
    )

    return parser


def main():
    parser = create_parsers()
    args = parser.parse_args()

    if args.command == "calc":
        try:
            result = start_calculator(args.expression)  # запуск калькулятора

            save_history_of_successful_calculation(
                args.command, args.expression, result
            )

            print(f"Результат: {result}")
            sys.exit(0)
        except CalculatorErrors as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        try:
            result = start_converter(
                args.value, args.unit_from, args.unit_to
            )  # запуск конвертера

            save_history_of_successful_conversion(
                args.command, args.value, args.unit_from, args.unit_to, result
            )

            print(f"Результат: {result}")
            sys.exit(0)
        except ConverterErrors as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
