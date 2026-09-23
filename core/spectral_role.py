from enum import Enum


class SpectralRole(Enum):
    COASTAL = "coastal"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    RED_EDGE_1 = "red_edge_1"
    RED_EDGE_2 = "red_edge_2"
    RED_EDGE_3 = "red_edge_3"
    NIR = "nir"
    NARROW_NIR = "narrow_nir"
    WATER_VAPOR = "water_vapor"
    SWIR1 = "swir1"
    SWIR2 = "swir2"
    PAN = "pan"
    CIRRUS = "cirrus"
    TIRS1 = "tirs1"
    TIRS2 = "tirs2"
    QA = "qa"
