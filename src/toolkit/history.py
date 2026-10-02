import json
import os

from .constants import HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE


def save_history_of_successful_calculation(
    command: str, input_data: str, result: str
) -> None:
    """Сохранение истории успешных операций для калькулятора"""
    calculation = {"command": command, "input_data": input_data, "result": result}
    history = []

    if os.path.isfile(HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE):
        try:
            with open(
                HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE, "r", encoding="utf-8"
            ) as f:
                history = json.load(f)
        except Exception:
            pass

    history.append(calculation)

    with open(HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def save_history_of_successful_conversion(
    command: str, input_data: str, unit_from: str, unit_to: str, result: str
) -> None:
    """Сохранение истории успешных операций для конвертера"""
    conversion = {
        "command": command,
        "input_data": input_data,
        "unit_from": unit_from,
        "unit_to": unit_to,
        "result": result,
    }
    history = []

    if os.path.isfile(HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE):
        try:
            with open(
                HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE, "r", encoding="utf-8"
            ) as f:
                history = json.load(f)
        except Exception:
            pass

    history.append(conversion)
    with open(HISTORY_OF_SUCCESSFUL_COMPUTATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
