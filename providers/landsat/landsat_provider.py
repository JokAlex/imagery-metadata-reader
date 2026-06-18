from pathlib import Path

from .landsat_product import LandsatProduct


class LandsatProvider:
    def can_open(
        self,
        path: Path
    ) -> bool:
        for file in path.iterdir():

            if file.name.endswith(
                "_MTL.txt"
            ):
                return True

        return False

    def open(
        self,
        path: Path
    ) -> LandsatProduct:
        return LandsatProduct(path)
