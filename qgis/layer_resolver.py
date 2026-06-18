from pathlib import Path

from qgis.core import QgsRasterLayer


class LayerResolver:
    def product_root(
        self,
        layer: QgsRasterLayer
    ) -> Path:

        raster_path = Path(
            layer.source()
        )

        return raster_path.parent
