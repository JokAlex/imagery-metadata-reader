from imagery_metadata_reader import QgsLayerResolver, SpectralRole
from qgis.utils import iface

product = QgsLayerResolver.open_product(iface.activeLayer())

print("Product type:", type(product).__name__)
print("Acquisition time:", product.acquisition_time())
print("Cloud cover (%):", product.cloud_cover())

red_edge = product.band_by_role(SpectralRole.RED_EDGE_1)
print("Path to band Red Edge 1:", red_edge.path())
print("Resolution of Red Edge 1:", red_edge.resolution())

print("Product URI:", product["Product_Info/PRODUCT_URI"])
