from decimal import Decimal

import pytest

from toolkit.converter import start_converter
from toolkit.errors import (
    DifferentUnitsError,
    InvalidUnitError,
    UnderAbsoluteZeroTemperatureError,
)


def test_converter_distance() -> None:
    assert start_converter(Decimal("30"), "m", "cm") == Decimal("3000.0")
    assert start_converter(Decimal("1000"), "Km", "M") == Decimal("1000000.0")
    assert start_converter(Decimal("250"), "mm", "m") == Decimal("0.25")
    assert start_converter(Decimal("500"), "cm", "cm") == Decimal("500.0")


def test_converter_temperature() -> None:
    assert start_converter(Decimal("250"), "K", "k") == Decimal("250.0")
    assert start_converter(Decimal("500"), "c", "k") == Decimal("773.15")


def test_converter_weight() -> None:
    assert start_converter(Decimal("250"), "kg", "kG") == Decimal("250.0")
    assert start_converter(Decimal("1000"), "g", "KG") == Decimal("1.0")
    assert start_converter(Decimal("2"), "kg", "g") == Decimal("2000.0")


def test_converter_invalid_unit() -> None:
    with pytest.raises(InvalidUnitError):
        start_converter(Decimal("250"), "WW", "G")


def test_converter_different_units() -> None:
    with pytest.raises(DifferentUnitsError):
        start_converter(Decimal("10"), "cm", "G")


def test_converter_under_absolute_zero() -> None:
    with pytest.raises(UnderAbsoluteZeroTemperatureError):
        start_converter(Decimal("-280"), "c", "f")
