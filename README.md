# Imagery Metadata Reader

Imagery Metadata Reader is a plugin for QGIS that allows you to extract metadata from Landsat 8-9 satellite images.

## Usage example

```python
from imagery_metadata_reader import (
    LayerResolver, LandsatProvider, SpectralRole
)

# First of all, you should create an instance of LayerResolver
resolver = LayerResolver()

# With resolver you can get directory of image
product_dir = resolver.product_root(raster_layer)

# For reading and accessing metadata you should create provider 
# for satellite imagery system of your image
provider = LandsatProvider()
product = provider.open(product_dir)

metadata = product.metadata()

# When you got metadata object, you can extract data from its fields
print("Acquisition time =", metadata.acquisition_time)

# Or as from dictionary:
print("Origin:", metadata["ORIGIN"])

# Also, you can get each available band from product:
nir = product.band_by_role(SpectralRole.SWIR1)

print("Path to NIR band file =", nir.path)
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
