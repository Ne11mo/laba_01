from toolkit.converter import start_converter
from toolkit.errors import (
    DifferentUnitsError,
    InvalidUnitError,
    UnderAbsoluteZeroTemperatureError,
)


def test_converter_distance() -> None:
    assert start_converter(30, "m", "cm") == 3000.0
    assert start_converter(1000, "Km", "M") == 1000000.0
    assert start_converter(250, "mm", "m") == 0.25
    assert start_converter(500, "cm", "cm") == 500.0


def test_converter_temperature() -> None:
    assert start_converter(250, "K", "k") == 250.0
    assert start_converter(500, "c", "k") == 773.15


def test_converter_weight() -> None:
    assert start_converter(250, "kg", "kG") == 250.0
    assert start_converter(1000, "g", "KG") == 1.0
    assert start_converter(2, "kg", "g") == 2000.0


def test_converter_invalid_unit() -> None:
    result = start_converter(250, "WW", "G")
    assert isinstance(result, InvalidUnitError)


def test_converter_different_units() -> None:
    result = start_converter(10, "cm", "G")
    assert isinstance(result, DifferentUnitsError)


def test_converter_under_absolute_zero() -> None:
    result = start_converter(-280, "c", "f")
    assert isinstance(result, UnderAbsoluteZeroTemperatureError)
