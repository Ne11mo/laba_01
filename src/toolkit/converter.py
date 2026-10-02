from decimal import ROUND_HALF_UP, Decimal, getcontext

from .constants import AVAILABLE_UNITS, DISTANCE_UNITS, TEMPERATURE_UNITS, WEIGHT_UNITS
from .errors import (
    DifferentUnitsError,
    InvalidUnitError,
    UnderAbsoluteZeroTemperatureError,
)

getcontext().prec = 28


def validate_units(value: Decimal, unit_from: str, unit_to: str) -> None:
    if (unit_from not in AVAILABLE_UNITS) or (unit_to not in AVAILABLE_UNITS):
        raise InvalidUnitError("Недопустимая единица")

    if (
        unit_from in TEMPERATURE_UNITS
        and unit_to not in TEMPERATURE_UNITS
        or unit_from in DISTANCE_UNITS
        and unit_to not in DISTANCE_UNITS
        or unit_from in WEIGHT_UNITS
        and unit_to not in WEIGHT_UNITS
    ):
        raise DifferentUnitsError("Несовместимые единицы")

    if (
        unit_from in TEMPERATURE_UNITS
        and (unit_from == "k" and value < Decimal("0"))
        or (unit_from == "c" and value < Decimal("-273.15"))
        or (unit_from == "f" and value < Decimal("-459.67"))
    ):
        raise UnderAbsoluteZeroTemperatureError(
            "Температура ниже абсолютного нуля запрещена"
        )


def convert_temperature_units(value: Decimal, unit_from: str, unit_to: str) -> Decimal:
    if unit_from == "c":
        if unit_to == "c":
            return value
        elif unit_to == "f":
            return value * Decimal("1.8") + Decimal("32")
        else:
            return value + Decimal("273.15")
    elif unit_from == "f":
        if unit_to == "f":
            return value
        elif unit_to == "c":
            return (value - Decimal("32")) / Decimal("1.8")
        else:
            return (value - Decimal("32")) / Decimal("1.8") + Decimal("273.15")
    else:
        if unit_to == "k":
            return value
        elif unit_to == "c":
            return value - Decimal("273.15")
        else:
            return (value - Decimal("273.15")) * Decimal("1.8") + Decimal("32")


def convert_distance_units(value: Decimal, unit_from: str, unit_to: str) -> Decimal:
    result = value
    if unit_from == "mm" and unit_to != "mm":
        if unit_to == "cm":
            result = value / Decimal("10.0")
        elif unit_to == "m":
            result = value / Decimal("1000.0")
        else:
            result = value / Decimal("1000000.0")
    elif unit_from == "cm" and unit_to != "cm":
        if unit_to == "mm":
            result = value * Decimal("10.0")
        elif unit_to == "m":
            result = value / Decimal("100.0")
        else:
            result = value / Decimal("100000.0")
    elif unit_from == "m" and unit_to != "m":
        if unit_to == "mm":
            result = value * Decimal("1000.0")
        elif unit_to == "cm":
            result = value * Decimal("100.0")
        else:
            result = value / Decimal("1000.0")
    elif unit_from == "km" and unit_to != "km":
        if unit_to == "mm":
            result = value * Decimal("1000000.0")
        elif unit_to == "cm":
            result = value * Decimal("100000.0")
        else:
            result = value * Decimal("1000.0")

    result = result.quantize(Decimal("0.0000000001"), ROUND_HALF_UP).normalize()
    return result


def convert_weight_units(value: Decimal, unit_from: str, unit_to: str) -> Decimal:
    result = value
    if unit_from == "g" and unit_to == "kg":
        result = value / Decimal("1000.0")
    elif unit_from == "kg" and unit_to == "g":
        result = value * Decimal("1000.0")

    result = result.quantize(Decimal("0.0000000001"), ROUND_HALF_UP).normalize()
    return result


def start_converter(value: Decimal, unit_from: str, unit_to: str) -> Decimal:
    unit_from = unit_from.lower()
    unit_to = unit_to.lower()

    validate_units(value, unit_from, unit_to)

    if unit_from in TEMPERATURE_UNITS:
        return convert_temperature_units(value, unit_from, unit_to)
    elif unit_from in DISTANCE_UNITS:
        return convert_distance_units(value, unit_from, unit_to)
    else:
        return convert_weight_units(value, unit_from, unit_to)
