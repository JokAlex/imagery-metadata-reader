from abc import abstractmethod

from .provider import ProductProvider
from .exceptions import UnsupportedProductError


class ProviderRegistry(ProductProvider):
    @abstractmethod
    def register(self, provider):
        ...
