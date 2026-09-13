from imagery_metadata_reader import LandsatProvider, QgsLayerResolver, SpectralRole
from qgis.utils import iface


product = QgsLayerResolver.open_product(iface.activeLayer())

print("Acquisition time =", product.acquisition_time())
print("Cloud cover =", product.cloud_cover())

nir = product.band_by_role(
    SpectralRole.NIR
)

print("Path to NIR band file =", nir.path())
print("Spatial resolution of NIR band =", nir.resolution())
print("Origin:", product["ORIGIN"])
