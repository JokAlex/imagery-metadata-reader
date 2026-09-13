from abc import abstractmethod

from .product import ImageryProduct


class SpectralProduct(ImageryProduct):
    @abstractmethod
    def cloud_cover(self) -> float:
        ...
