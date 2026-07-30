from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib # Python version lower than 3.11

PATTERNS_FILE = Path(__file__).parent / "patterns.toml"

@dataclass
class Pattern:
    name: str
    alive_cells : set[tuple[int, int]]

    @classmethod
    def from_toml(cls, name, toml_data):
        return cls(
            name=name,
            alive_cells={tuple(cell) for cell in toml_data["alive_cells"]},
        )

def get_pattern(name: str, filename:str = PATTERNS_FILE) -> Pattern:
    """
    This function takes the name of a target pattern and the name of the TOML file as arguments and returns a Pattern instance representing the pattern whose name matches the name argument.
    """
    data = tomllib.loads(filename.read_text(encoding="utf-8"))

    return Pattern.from_toml(name=name, toml_data=data[name])

def get_all_patterns(filename:str = PATTERNS_FILE) -> list[Pattern]:
    """
    This function takes the name of the TOML file as an argument and returns a list of Pattern instances representing all the patterns defined in the TOML file.
    """
    data = tomllib.loads(filename.read_text(encoding="utf-8"))

    return [
        Pattern.from_toml(name=name, toml_data=toml_data) for name, toml_data in data.items()
    ]
