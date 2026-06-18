from imagery_metadata_reader import LandsatProvider
from imagery_metadata_reader import LayerResolver
from imagery_metadata_reader import SpectralRole
from qgis.utils import iface

raster_layer = iface.activeLayer()

resolver = LayerResolver()

product_dir = resolver.product_root(
    raster_layer
)

provider = LandsatProvider()

product = provider.open(
    product_dir
)

metadata = product.metadata()

print("Acquisition time =", metadata.acquisition_time)
print("Cloud cover =", metadata.cloud_cover)

nir = product.band_by_role(
    SpectralRole.SWIR1
)

print("Path to NIR band file =", nir.path)
print("Origin:", metadata["ORIGIN"])
