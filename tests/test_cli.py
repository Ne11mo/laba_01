import subprocess


def test_cli_calc():
    result = subprocess.run(
        ["python", "-m", "toolkit", "calc", "2 + 2 * 2"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Результат: 6.0" in result.stdout


def test_cli_converter():
    result = subprocess.run(
        ["python", "-m", "toolkit", "convert", "36", "--from", "c", "--to", "F"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Результат: 96.8" in result.stdout
