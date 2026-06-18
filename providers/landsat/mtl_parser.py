from pathlib import Path


class LandsatMtlParser:
    def __init__(self, mtl_path: Path):
        self._mtl_path = mtl_path

    def parse(self) -> dict:
        result = {}

        with self._mtl_path.open(
            "r",
            encoding="utf-8"
        ) as f:
            for line in f:
                line = line.strip()

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip().strip('"')

                if key == 'GROUP' or key == 'END_GROUP' or value == "":
                    continue

                result[key] = value

        return result
