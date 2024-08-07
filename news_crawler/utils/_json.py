from typing import Any


def load_json_file(json_filepath: str) -> Any:
    with open(json_filepath, mode="r+", encoding="UTF-8") as json_file:
        from json import load

        return load(json_file)


def write_json_file(json_filepath: str, obj: Any) -> None:
    with open(json_filepath, mode="w+", encoding="UTF-8") as json_file:
        from json import dumps

        json_file.write(dumps(obj, ensure_ascii=False))
