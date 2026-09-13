from datetime import datetime
from pathlib import Path
from typing import Sequence

from ...core.multispectral_band import MultispectralBand
from ...core.multispectral_product import MultispectralProduct
from ...core.spectral_role import SpectralRole

from .mtl_parser import LandsatMtlParser
from .landsat_datetime import parse_landsat_datetime


class LandsatProduct(MultispectralProduct):
    ROLE_MAP = {
        "BAND_1": SpectralRole.COASTAL,
        "BAND_2": SpectralRole.BLUE,
        "BAND_3": SpectralRole.GREEN,
        "BAND_4": SpectralRole.RED,
        "BAND_5": SpectralRole.NIR,
        "BAND_6": SpectralRole.SWIR1,
        "BAND_7": SpectralRole.SWIR2,
        "BAND_8": SpectralRole.PAN,
        "BAND_9": SpectralRole.CIRRUS,
        "BAND_10": SpectralRole.TIRS1,
        "BAND_11": SpectralRole.TIRS2,
        "QUALITY_L1_PIXEL": SpectralRole.QA,
    }

    RESOLUTIONS = {
        SpectralRole.COASTAL: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.BLUE: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.GREEN: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.RED: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.NIR: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.SWIR1: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.SWIR2: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.PAN: "GRID_CELL_SIZE_PANCHROMATIC",
        SpectralRole.CIRRUS: "GRID_CELL_SIZE_REFLECTIVE",
        SpectralRole.TIRS1: "GRID_CELL_SIZE_THERMAL",
        SpectralRole.TIRS2: "GRID_CELL_SIZE_THERMAL",
        SpectralRole.QA: "GRID_CELL_SIZE_REFLECTIVE",
    }

    def __init__(self, product_dir: Path):
        self._product_dir = product_dir
        self._base_path = ''

        self._mtl_file = self._find_mtl()

        parser = LandsatMtlParser(self._mtl_file)
        self._data = parser.parse()
        self._bands = tuple(self._parse_bands())
        self._acquisition_time = parse_landsat_datetime(
            self._data["DATE_ACQUIRED"],
            self._data["SCENE_CENTER_TIME"]
        )
        self._cloud_cover = float(self._data["CLOUD_COVER"])

    def _find_mtl(self) -> Path:
        for file in self._product_dir.iterdir():

            if file.name.endswith("_MTL.txt"):
                self._base_path = self._product_dir / file.name.removesuffix("_MTL.txt")
                return file

        raise FileNotFoundError(
            "MTL file not found"
        )

    def _parse_bands(self) -> Sequence[MultispectralBand]:
        bands = []

        for index, (band_id, role) in enumerate(self.ROLE_MAP.items()):
            file_name = self._data.get(f"FILE_NAME_{band_id}", None)

            if file_name is None:
                continue

            file_name = self._product_dir / file_name

            if not Path(file_name).is_file():
                continue

            resolution = float(self._data[self.RESOLUTIONS[role]])

            bands.append(
                MultispectralBand(
                    index=index,
                    role=role,
                    path=file_name,
                    resolution=(resolution, resolution)
                )
            )
        return bands

    def bands(self) -> Sequence[MultispectralBand]:
        return self._bands

    def band_by_role(self, role: SpectralRole) -> MultispectralBand:
        for band in self._bands:
            if band.role() == role:
                return band

        raise KeyError(role)
    
    def __getitem__(self, key: str) -> str:
        return self._data[key]

    def root(self) -> Path:
        return self._product_dir

    def acquisition_time(self) -> datetime:
        return self._acquisition_time

    def cloud_cover(self) -> float:
        return self._cloud_cover
