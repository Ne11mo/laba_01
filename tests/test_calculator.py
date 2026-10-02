from decimal import Decimal

import pytest

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
    assert start_calculator("2 + 2 * 2") == Decimal("6.0")
    assert start_calculator("(2 + 2) * 2") == Decimal("8.0")
    assert start_calculator("-(1 + 5) * 3") == Decimal("-18.0")


def test_calculation_basic_operations() -> None:
    assert start_calculator("1 + 1") == Decimal("2.0")
    assert start_calculator("4 - 1.5") == Decimal("2.5")
    assert start_calculator("4 // 3") == Decimal("1.0")
    assert start_calculator("4 - --3") == Decimal("1.0")
    assert start_calculator("5 * 5") == Decimal("25.0")
    assert start_calculator("5 % 3") == Decimal("2.0")


def test_calculation_expression() -> None:
    assert start_calculator("-(10 + 5*(2-4)) // 3") == Decimal("0.0")
    assert start_calculator("----++--10 % (2 + 4) *5") == Decimal("20.0")
    assert start_calculator("+(-(--2))*       25") == Decimal("-50.0")
    assert start_calculator("200 * (100 - 50 * 2) - 33.5 * 2") == Decimal("-67.0")
    assert start_calculator("2") == Decimal("2.0")


def test_calculation_division_by_zero() -> None:
    with pytest.raises(DivisionByZeroError):
        start_calculator("20 + 3 - 5 / 0")


def test_calculation_brackets() -> None:
    with pytest.raises(BracketsError):
        start_calculator("(1))")


def test_calculation_empty_expression() -> None:
    with pytest.raises(EmptyExpressionError):
        start_calculator("      ")


def test_calculation_invalid_character() -> None:
    with pytest.raises(InvalidCharacterError):
        start_calculator("12 - a")


def test_calculation_invalid_empty_operand() -> None:
    with pytest.raises(InvalidExpressionError):
        start_calculator("1 + ")


def test_calculation_double_binary_operation() -> None:
    with pytest.raises(DoubleBinaryOperationError):
        start_calculator("1 + 2 * * 3")


def test_calculation_invalid_expression() -> None:
    with pytest.raises(InvalidExpressionError):
        start_calculator("2 + (5 * )")


def test_calculation_empty_operation() -> None:
    with pytest.raises(EmptyOperationError):
        start_calculator("1 1")


def test_calculation_invalid_number() -> None:
    with pytest.raises(InvalidNumberError):
        start_calculator("1 + 2.1.1")
