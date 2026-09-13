from pathlib import Path

from ...core.exceptions import ProductNotFoundError
from ...core.provider import ProductProvider

from .landsat_product import LandsatProduct


class LandsatProvider(ProductProvider):
    def can_open(self, path: Path) -> bool:
        for file in path.iterdir():

            if file.name.endswith("_MTL.txt"):
                return True

        return False

    def open(self, path: Path) -> LandsatProduct:
        return LandsatProduct(self._find_root(path))
    
    def _find_root(self, source: Path) -> Path:
        directory = source if source.is_dir() else source.parent

        for path in [directory, *directory.parents]:
            mtl_files = list(path.glob("*_MTL.txt"))

            if mtl_files:
                return path

        raise ProductNotFoundError(
            f"Cannot locate Landsat product from {source}"
        )
