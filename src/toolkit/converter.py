from .constans import AVAILABLE_UNITS, TEMPERATURE_UNITS, DISTANCE_UNITS, WEIGHT_UNITS
from .errors import (
    ConverterErrors,
    InvalidUnitError,
    DifferentUnitsError,
    UnderAbsoluteZeroTemperatureError
)

def validate_units(value, unit_from, unit_to):
    if (unit_from not in AVAILABLE_UNITS) or (unit_to not in AVAILABLE_UNITS):
        raise InvalidUnitError("Недопустимая единица")

    if unit_from in TEMPERATURE_UNITS and unit_to not in TEMPERATURE_UNITS:
        raise DifferentUnitsError("Несовместимые единицы")
    elif unit_from in DISTANCE_UNITS and unit_to not in DISTANCE_UNITS:
        raise DifferentUnitsError("Несовместимые единицы")
    elif unit_from in WEIGHT_UNITS and unit_to not in WEIGHT_UNITS:
        raise DifferentUnitsError("Несовместимые единицы")

    if unit_from in TEMPERATURE_UNITS:
        if (unit_from == 'K' and value < 0) or (unit_from == 'c' and value < -273.15) or (unit_from == 'f' and value < -459.67):
            raise UnderAbsoluteZeroTemperatureError("Температура ниже абсолютного нуля запрещена")


def convert_temperature_units(value, unit_from, unit_to):
    if unit_from == 'c':
        if unit_to == 'c':
            return value
        elif unit_to == 'f':
            return value * 1.8 + 32
        else:
            return value + 273.15
    elif unit_from == 'f':
        if unit_to == 'f':
            return value
        elif unit_to == 'c':
            return (value - 32) / 1.8
        else:
            return (value - 32) / 1.8 + 273.15
    else:
        if unit_to == 'k':
            return value
        elif unit_to == 'c':
            return value - 273.15
        else:
            return (value - 273.15) * 1.8 + 32


def convert_distance_units(value, unit_from, unit_to):
    if unit_from == 'mm':
        if unit_to == 'mm':
            return value
        elif unit_to == 'cm':
            return value / 10.0
        elif unit_to == 'm':
            return value / 1000.0
        else:
            return value / 1000000.0
    elif unit_from == 'cm':
        if unit_to == 'cm':
            return value
        elif unit_to == 'mm':
            return value * 10.0
        elif unit_to == 'm':
            return value / 100.0
        else:
            return value / 100000.0
    elif unit_from == 'm':
        if unit_to == 'm':
            return value
        elif unit_to == 'mm':
            return value * 1000.0
        elif unit_to == 'cm':
            return value * 100.0
        else:
            return value / 1000.0
    else:
        if unit_to == 'km':
            return value
        elif unit_to == 'mm':
            return value * 1000000.0
        elif unit_to == 'cm':
            return value * 100000.0
        else:
            return value * 1000.0


def convert_weight_units(value, unit_from, unit_to):
    if unit_from == 'g':
        if unit_to == 'g':
            return value
        else:
            return value / 1000.0
    else:
        if unit_to == 'kg':
            return value
        else:
            return value * 1000.0


def start_converter(value, unit_from, unit_to):
    try:
        unit_from = unit_from.lower()
        unit_to = unit_to.lower()

        validate_units(value, unit_from, unit_to)

        if unit_from in TEMPERATURE_UNITS:
            return convert_temperature_units(value, unit_from, unit_to)
        elif unit_from in DISTANCE_UNITS:
            return convert_distance_units(value, unit_from, unit_to)
        else:
            return convert_weight_units(value, unit_from, unit_to)
    #различные ошибки, выбрасываемые конвертером
    except ConverterErrors as e:
        return e