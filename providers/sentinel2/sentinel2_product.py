import re
from datetime import datetime
from pathlib import Path
from typing import Sequence, Optional

from ...core.multispectral_band import MultispectralBand
from ...core.multispectral_product import MultispectralProduct
from ...core.spectral_role import SpectralRole

from .sentinel2_metadata_parser import Sentinel2MetadataParser


_BAND_NAME_RE = re.compile(r"_(B(?:0[1-9]|1[0-2]|8A)|TCI)(?:_|$)")


class Sentinel2Product(MultispectralProduct):
    ROLE_MAP = {
        "B01": SpectralRole.COASTAL,
        "B02": SpectralRole.BLUE,
        "B03": SpectralRole.GREEN,
        "B04": SpectralRole.RED,
        "B05": SpectralRole.RED_EDGE_1,
        "B06": SpectralRole.RED_EDGE_2,
        "B07": SpectralRole.RED_EDGE_3,
        "B08": SpectralRole.NIR,
        "B8A": SpectralRole.NARROW_NIR,
        "B09": SpectralRole.WATER_VAPOR,
        "B10": SpectralRole.CIRRUS,
        "B11": SpectralRole.SWIR1,
        "B12": SpectralRole.SWIR2,
    }

    BAND_RESOLUTIONS = {
        "B01": 60,
        "B02": 10,
        "B03": 10,
        "B04": 10,
        "B05": 20,
        "B06": 20,
        "B07": 20,
        "B08": 10,
        "B8A": 20,
        "B09": 60,
        "B10": 60,
        "B11": 20,
        "B12": 20,
    }

    def __init__(self, product_dir: Path):
        self._product_dir = product_dir
        self._metadata_file = self._find_metadata()
        parser = Sentinel2MetadataParser(self._metadata_file)
        self._data = parser.parse()
        self._bands = tuple(self._parse_bands())
        self._acquisition_time = self._parse_acquisition_time()
        self._cloud_cover = self._parse_cloud_cover()

    def _find_metadata(self) -> Path:
        for pattern in ("MTD_MSIL2A.xml", "MTD_MSIL1C.xml"):
            candidate = self._product_dir / pattern
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(
            f"Sentinel-2 metadata file was not found at {self._product_dir}"
        )

    def _parse_bands(self) -> Sequence[MultispectralBand]:
        bands = []
        image_files = self._find_all("IMAGE_FILE")

        for rel in image_files:
            name = rel.rsplit("/", 1)[-1]
            match = _BAND_NAME_RE.search(name)
            if match is None:
                continue
            band_name = match.group(1)
            if band_name not in self.ROLE_MAP:
                continue

            path = self._product_dir / f"{rel}.jp2"
            if not path.is_file():
                path = self._product_dir / rel
            if not path.is_file():
                continue

            resolution = self.BAND_RESOLUTIONS.get(band_name, 10)
            bands.append(
                MultispectralBand(
                    index=len(bands),
                    role=self.ROLE_MAP[band_name],
                    path=path,
                    resolution=(float(resolution), float(resolution)),
                )
            )
        return bands

    def _find(self, *suffixes: str) -> Optional[str]:
        for suffix in suffixes:
            for key, value in self._data.items():
                if key == suffix or key.endswith(f"/{suffix}"):
                    return value
        return None
    
    def _find_all(self, *suffixes: str) -> list[str]:
        result: list[str] = []
        for suffix in suffixes:
            for key, value in self._data.items():
                if key == suffix or key.endswith(f"/{suffix}"):
                    if isinstance(value, list):
                        result.extend(value)
                    else:
                        result.append(value)
        return result

    def _parse_acquisition_time(self) -> datetime:
        raw = self._find("PRODUCT_START_TIME")
        if raw is None:
            raise KeyError(
                "Cannot find acquisition time in Sentinel-2 metadata. "
                f"Available keys: {sorted(self._data)[:20]}..."
            )
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        return datetime.fromisoformat(raw)

    def _parse_cloud_cover(self) -> float:
        raw = self._find("Cloud_Coverage_Assessment")
        return float(raw) if raw is not None else 0.0

    def bands(self) -> Sequence[MultispectralBand]:
        return self._bands

    def band_by_role(self, role: SpectralRole) -> MultispectralBand:
        for band in self._bands:
            if band.role() == role:
                return band
        raise KeyError(role)

    def __getitem__(self, key: str) -> str:
        value = self._find(key)
        if value is None:
            raise KeyError(key)
        return value

    def root(self) -> Path:
        return self._product_dir

    def acquisition_time(self) -> datetime:
        return self._acquisition_time

    def cloud_cover(self) -> float:
        return self._cloud_cover
