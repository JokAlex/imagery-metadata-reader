from pathlib import Path

from ..core.product import ImageryProduct
from ..core.provider_catalog import ProviderCatalog
from ..core.provider import ProductProvider
from qgis.core import QgsRasterLayer


class QgsLayerResolver:
    @staticmethod
    def product_root(layer: QgsRasterLayer) -> Path:
        raster_path = Path(layer.source())
        return raster_path.parent

    @staticmethod
    def open_product(
        layer: QgsRasterLayer, 
        handler: ProductProvider = ProviderCatalog.default()
    ) -> ImageryProduct:
        return handler.open(QgsLayerResolver.product_root(layer))
