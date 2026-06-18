from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Optional


class BandType(Enum):
    SPECTRAL = auto()
    SAR = auto()
    ELEVATION = auto()
    TEMPERATURE = auto()


class SpectralRole(Enum):
    BLUE = auto()
    GREEN = auto()
    RED = auto()
    NIR = auto()
    SWIR1 = auto()
    SWIR2 = auto()
    PAN = auto()
    COASTAL = auto()
    CIRRUS = auto()
    TIRS1 = auto()
    TIRS2 = auto()


@dataclass
class SpectralBand:
    id: str

    center_wavelength_nm: float

    bandwidth_nm: float

    resolution_m: float

    path: Path
    role: Optional[SpectralRole]


class BandName(Enum):
    BLUE = auto()
    GREEN = auto()
    RED = auto()

    NIR = auto()

    SWIR1 = auto()
    SWIR2 = auto()

    PAN = auto()

    VV = auto()
    VH = auto()


@dataclass(frozen=True)
class BandInfo:
    name: BandName

    path: Path

    wavelength_min: Optional[float]
    wavelength_max: Optional[float]

    resolution: float
