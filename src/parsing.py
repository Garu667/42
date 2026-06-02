from pydantic import BaseModel, Field, model_validator
from typing import Any


class MissingKeyError(Exception):
    pass


class PositionError(Exception):
    pass


class FileNameError(Exception):
    pass


class Parsing(BaseModel):
    width: int = Field(ge=3, le=200)
    height: int = Field(ge=3, le=200)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=5, max_length=50)
    perfect: bool = True
    seed: int = Field(ge=0)

    @model_validator(mode='before')
    @classmethod
    def dict_validator(cls, data: dict[str, Any]) -> dict[str, Any]:
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
                "SEED"]
        for key in keys:
            if key not in data:
                raise MissingKeyError(f"Missing key '{key}' in config file")
            if not data[key] or not data[key].strip():
                raise ValueError(f"Key '{key}' exists but has no value in "
                                 "config file")
        try:
            data["WIDTH"] = int(data["WIDTH"].strip())
            data["HEIGHT"] = int(data["HEIGHT"].strip())
            data["SEED"] = int(data["SEED"].strip())
        except ValueError:
            raise ValueError("WIDTH, HEIGHT and SEED must be valid integers")
        try:
            entry_position = [nb.strip() for nb in data["ENTRY"].split(',')]
            exit_position = [nb.strip() for nb in data["EXIT"].split(',')]
            if len(entry_position) != 2 or len(exit_position) != 2:
                raise ValueError("ENTRY and EXIT must follow the 'x,y' format")
            data["ENTRY"] = tuple(int(nb) for nb in entry_position)
            data["EXIT"] = tuple(int(nb) for nb in exit_position)
        except ValueError as e:
            raise ValueError(f"Invalid ENTRY or EXIT format: {e}")
        perfect_value = data["PERFECT"].strip().lower()
        if perfect_value not in ("true", "false"):
            raise ValueError("PERFECT value must be 'True' or 'False'")
        return {"width": data["WIDTH"], "height": data["HEIGHT"],
                "entry": data["ENTRY"], "exit": data["EXIT"],
                "output_file": data["OUTPUT_FILE"].strip(),
                "perfect": perfect_value == "true",
                "seed": data["SEED"]}

    @model_validator(mode='after')
    def config_validator(self) -> 'Parsing':
        if self.entry[0] < 0 or self.entry[1] < 0:
            raise PositionError("Entry position coordinates must be "
                                "non-negative")
        if self.entry[0] >= self.width or self.entry[1] >= self.height:
            raise PositionError(f"Entry position {self.entry} is out of "
                                f"grid bounds ({self.width}x{self.height})")
        if self.exit[0] < 0 or self.exit[1] < 0:
            raise PositionError("Exit position coordinates must be "
                                "non-negative")
        if self.exit[0] >= self.width or self.exit[1] >= self.height:
            raise PositionError(f"Exit position {self.exit} is out of "
                                f"grid bounds ({self.width}x{self.height})")
        if self.entry == self.exit:
            raise PositionError("Entry and exit positions must be different")
        if not self.output_file.endswith(".txt"):
            raise FileNameError("Output file must have a '.txt' extension.")
        return self
