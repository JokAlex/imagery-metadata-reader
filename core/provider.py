from abc import ABC, abstractmethod
from pathlib import Path

from .product import ImageryProduct


class ProductProvider(ABC):
    @abstractmethod
    def open(self, path: Path) -> ImageryProduct:
        ...
