from abc import ABC, abstractmethod

from core.metadata import ProductMetadata
from core.bands import BandInfo, BandName

class SatelliteProduct(ABC):

    @abstractmethod
    def metadata(self) -> ProductMetadata:
        ...
    
    @abstractmethod
    def __getitem__(self, key: str) -> str:
        ...

    @abstractmethod
    def bands(self) -> list[BandInfo]:
        ...

    @abstractmethod
    def band(self, band: BandName) -> BandInfo:
        ...
