from pathlib import Path
from typing import Iterable

from .exceptions import ProductNotFoundError
from .provider_registry import ProviderRegistry
from .product import ImageryProduct
from .provider import ProductProvider

from ..providers import landsat, sentinel2


class ProviderCatalog(ProviderRegistry):
    def __init__(self, providers: Iterable[ProductProvider]) -> None:
        self._providers = list(providers)

    def register(self, provider) -> None:
        self._providers.append(provider)
        
    def open(self, source: Path) -> ImageryProduct:
        for provider in self._providers:
            try:
                return provider.open(source)
            except ProductNotFoundError:
                pass

        raise ProductNotFoundError(source)

    @staticmethod
    def default() -> ProductProvider:
        return ProviderCatalog([
            landsat.LandsatProvider(),
            sentinel2.Sentinel2Provider(),
        ])
