from toolkit.calculator import start_calculator
from toolkit.errors import (
    BracketsError,
    DivisionByZeroError,
    DoubleBinaryOperationError,
    EmptyExpressionError,
    EmptyOperationError,
    InvalidCharacterError,
    InvalidExpressionError,
    InvalidNumberError,
)
from toolkit.tokenization import (
    recognize_unary_operators_for_finally_tokens,
    tokenization,
)


def test_tokenization() -> None:
    assert tokenization("") == []
    assert tokenization("1 + 2 - 3") == ["1", "+", "2", "-", "3"]
    assert tokenization("-(11111 - 54 * (3     - 1))") == [
        "$",
        "(",
        "11111",
        "-",
        "54",
        "*",
        "(",
        "3",
        "-",
        "1",
        ")",
        ")",
    ]


def test_finally_tokenization() -> None:
    assert recognize_unary_operators_for_finally_tokens(
        ["+", "-", "-", "2", "*", "33"]
    ) == ["@", "2", "*", "33"]
    assert recognize_unary_operators_for_finally_tokens(
        ["-", "2", "*", "-", "-", "-", "10", "!", "(", "3", "-", "1", ")"]
    ) == ["$", "2", "*", "$", "10", "!", "(", "3", "-", "1", ")"]
    assert recognize_unary_operators_for_finally_tokens(["2", "-", "-", "0.5"]) == [
        "2",
        "-",
        "$",
        "0.5",
    ]


def test_calculation_priority() -> None:
    assert start_calculator("2 + 2 * 2") == 6.0
    assert start_calculator("(2 + 2) * 2") == 8.0
    assert start_calculator("-(1 + 5) * 3") == -18.0


def test_calculation_basic_operations() -> None:
    assert start_calculator("1 + 1") == 2.0
    assert start_calculator("4 - 1.5") == 2.5
    assert start_calculator("4 // 3") == 1.0
    assert start_calculator("4 - --3") == 1.0
    assert start_calculator("5 * 5") == 25.0
    assert start_calculator("5 % 3") == 2.0


def test_calculation_expression() -> None:
    assert start_calculator("-(10 + 5*(2-4)) // 3") == 0.0
    assert start_calculator("----++--10 % (2 + 4) *5") == 20.0
    assert start_calculator("+(-(--2))*       25") == -50.0
    assert start_calculator("200 * (100 - 50 * 2) - 33.5 * 2") == -67.0
    assert start_calculator("2") == 2.0


def test_calculation_division_by_zero() -> None:
    result_1 = start_calculator("20 + 3 - 5 / 0")
    assert isinstance(result_1, DivisionByZeroError)

    result_2 = start_calculator("20 + ((2 - 3) / (1.5 - 1.5))")
    assert isinstance(result_2, DivisionByZeroError)


def test_calculation_brackets() -> None:
    result_1 = start_calculator("(1))")
    assert isinstance(result_1, BracketsError)

    result_2 = start_calculator(")1(")
    assert isinstance(result_2, BracketsError)


def test_calculation_empty_expression() -> None:
    result = start_calculator("      ")
    assert isinstance(result, EmptyExpressionError)


def test_calculation_invalid_character() -> None:
    result = start_calculator("12 - a")
    assert isinstance(result, InvalidCharacterError)


def test_calculation_invalid_empty_operand() -> None:
    result = start_calculator("1 + ")
    assert isinstance(result, InvalidExpressionError)


def test_calculation_double_binary_operation() -> None:
    result_1 = start_calculator("1 + 2 * * 3")
    assert isinstance(result_1, DoubleBinaryOperationError)

    result_2 = start_calculator("100 + % 10")
    assert isinstance(result_2, DoubleBinaryOperationError)


def test_calculation_invalid_expression() -> None:
    result = start_calculator("2 + (5 * )")
    assert isinstance(result, InvalidExpressionError)


def test_calculation_empty_operation() -> None:
    result = start_calculator("1 1")
    assert isinstance(result, EmptyOperationError)


def test_calculation_invalid_number() -> None:
    result_1 = start_calculator("1 + 2.1.1")
    assert isinstance(result_1, InvalidNumberError)

    result_2 = start_calculator("5 + .5")
    assert isinstance(result_2, InvalidNumberError)
