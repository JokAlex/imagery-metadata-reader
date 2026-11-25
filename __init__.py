from .core import *
from .providers import *


try:
    from .qgis import *

    class ImageryMetadataReaderPlugin:
        def __init__(self):
            pass

        def initGui(self):
            pass

        def unload(self):
            pass

    def classFactory(iface):
        return ImageryMetadataReaderPlugin()

except ImportError:
    pass
