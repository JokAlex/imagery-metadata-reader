from pathlib import Path
from datetime import datetime

from ...core.metadata import ProductMetadata
from ...core.channel import ProductChannel
from ...core.channel import SpectralRole

from .mtl_parser import LandsatMtlParser
from .landsat_datetime import parse_landsat_datetime


class LandsatProduct:
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

    def __init__(self, product_dir: Path):
        self._product_dir = product_dir
        self._base_path = ''

        self._mtl_file = self._find_mtl()

        parser = LandsatMtlParser(
            self._mtl_file
        )

        self._data = parser.parse()

    def _find_mtl(self) -> Path:
        for file in self._product_dir.iterdir():

            if file.name.endswith("_MTL.txt"):
                self._base_path = self._product_dir / file.name.removesuffix("_MTL.txt")
                return file

        raise FileNotFoundError(
            "MTL file not found"
        )

    def metadata(self) -> ProductMetadata:
        acquisition = parse_landsat_datetime(
            self._data["DATE_ACQUIRED"],
            self._data["SCENE_CENTER_TIME"]
        )

        return ProductMetadata(
            satellite=self._data.get(
                "SPACECRAFT_ID",
                ""
            ),
            sensor=self._data.get(
                "SENSOR_ID",
                ""
            ),
            acquisition_time=acquisition,
            cloud_cover=float(
                self._data["CLOUD_COVER"]
            ),
            sun_azimuth=float(
                self._data["SUN_AZIMUTH"]
            ),
            sun_elevation=float(
                self._data["SUN_ELEVATION"]
            ),
            processing_level=self._data.get(
                "PROCESSING_LEVEL"
            ),
            _data=self._data
        )

    def channels(self) -> list[ProductChannel]:
        channels = []

        for band_id, role in self.ROLE_MAP.items():
            file_name = self._data.get(f"FILE_NAME_{band_id}", None)

            if file_name is None:
                continue

            file_name = self._product_dir / file_name

            if not Path(file_name).is_file():
                continue

            channels.append(
                ProductChannel(
                    id=band_id,
                    role=role,
                    path=file_name
                )
            )

        return channels

    def channel(
        self,
        band_id: str
    ) -> ProductChannel:
        for channel in self.channels():

            if channel.id == band_id:
                return channel

        raise KeyError(band_id)

    def band_by_role(
        self,
        role: SpectralRole
    ) -> ProductChannel:
        for channel in self.channels():

            if channel.role == role:
                return channel

        raise KeyError(role)
    
    def __getitem__(self, key: str) -> str:
        return self._data[key]
