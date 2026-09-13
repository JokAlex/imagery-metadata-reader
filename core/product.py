from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Sequence

from .band import Band

class ImageryProduct(ABC):

    @abstractmethod
    def root(self) -> Path:
        ...

    @abstractmethod
    def __getitem__(self, key: str) -> str:
        ...

    @abstractmethod
    def bands(self) -> Sequence[Band]:
        ...
    
    @abstractmethod
    def acquisition_time(self) -> datetime:
        ...
