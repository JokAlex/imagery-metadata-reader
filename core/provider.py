from abc import ABC, abstractmethod
from pathlib import Path

from core.product import SatelliteProduct


class ProductProvider(ABC):
    @abstractmethod
    def can_open(self, path: Path) -> bool:
        ...

    @abstractmethod
    def open(self, path: Path) -> SatelliteProduct:
        ...
