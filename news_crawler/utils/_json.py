from typing import Any


def load_json_file(json_filepath: str) -> Any:
    with open(json_filepath, mode="r+", encoding="UTF-8") as json_file:
        from json import loads

        return loads(json_file.read())
