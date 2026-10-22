"""Environment and tooling verification test."""

import sys
from result import Err, Ok, Result
import game_of_life


def test_python_version() -> None:
    """Ensure running on Python 3.14+."""
    assert sys.version_info >= (3, 14), f"Expected Python 3.14+, got {sys.version}"


def test_result_package_import() -> None:
    """Ensure result package is available and functions as expected."""
    def divide(a: int, b: int) -> Result[int, str]:
        if b == 0:
            return Err("Division by zero")
        return Ok(a // b)

    ok_res = divide(10, 2)
    assert ok_res.is_ok()
    assert ok_res.ok() == 5

    err_res = divide(10, 0)
    assert err_res.is_err()
    assert err_res.err() == "Division by zero"


def test_package_import() -> None:
    """Ensure game_of_life package can be imported."""
    assert game_of_life.__version__ == "0.1.0"
