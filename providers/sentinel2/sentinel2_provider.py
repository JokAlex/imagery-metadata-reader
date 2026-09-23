# providers/sentinel2/sentinel2_provider.py
from pathlib import Path

from ...core.exceptions import ProductNotFoundError
from ...core.provider import ProductProvider

from .sentinel2_product import Sentinel2Product


class Sentinel2Provider(ProductProvider):
    METADATA_FILES = ("MTD_MSIL2A.xml", "MTD_MSIL1C.xml")

    def can_open(self, path: Path) -> bool:
        if not path.is_dir():
            return False
        return any((path / name).is_file() for name in self.METADATA_FILES)

    def open(self, path: Path) -> Sentinel2Product:
        root = self._find_root(path)
        return Sentinel2Product(root)

    def _find_root(self, source: Path) -> Path:
        directory = source if source.is_dir() else source.parent

        for path in [directory, *directory.parents]:
            if any((path / name).is_file() for name in self.METADATA_FILES):
                return path

        raise ProductNotFoundError(
            f"Could not found Sentinel-2 product root in {source}"
        )
