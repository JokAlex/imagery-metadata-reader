from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ProductMetadata:
    satellite: str
    sensor: str

    acquisition_time: datetime

    cloud_cover: Optional[float]

    sun_azimuth: Optional[float]
    sun_elevation: Optional[float]

    processing_level: Optional[str]

    _data: dict[str, str] = field(default_factory=dict)

    def __getitem__(self, key: str) -> str:
        return self._data[key]


@dataclass
class SpectralMetadata:

    spectral_range_min_nm: float

    spectral_range_max_nm: float

    spectral_sampling_nm: float

    fwhm_nm: list[float]
