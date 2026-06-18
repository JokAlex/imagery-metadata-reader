__author__ = 'JokAlex&Sirius'
__date__ = '2026-06-12'
__copyright__ = '(C) 2026 by JokAlex&Sirius'

from .core import *
from .providers import *
from .qgis import *


class ImageryMetadataReaderPlugin:
    def __init__(self):
        pass

    def initGui(self):
        pass

    def unload(self):
        pass


def classFactory(iface):
    """Load ImageryMetadataReader class from file ImageryMetadataReader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    return ImageryMetadataReaderPlugin()
