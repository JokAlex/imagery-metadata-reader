# Imagery Metadata Reader

Imagery Metadata Reader is a plugin for QGIS that allows you to extract metadata from Landsat 8-9 satellite images.

## Usage example

```python
from imagery_metadata_reader import (
    LandsatProvider, 
    QgsLayerResolver, 
    SpectralRole
)
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
```

For more examples see `examples` directory.

## Building a release

If you have `make`, you can build the plugin release with the command:

```bash
make release
```

Otherwise, you should use the Python script directly:

```bash
python ./scripts/release.py
```

Both actions will create a `.dist` directory containing the plugin's ZIP archive and a subdirectory containing its contents.
