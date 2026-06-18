from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from typing import Optional


class SpectralRole(Enum):
    COASTAL = "coastal"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    NIR = "nir"
    SWIR1 = "swir1"
    SWIR2 = "swir2"
    PAN = "pan"
    CIRRUS = "cirrus"
    TIRS1 = "tirs1"
    TIRS2 = "tirs2"
    QA = "qa"


@dataclass(frozen=True)
class ProductChannel:
    id: str
    path: Path
    role: Optional[SpectralRole]
