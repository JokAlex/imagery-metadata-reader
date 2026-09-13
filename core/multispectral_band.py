from pathlib import Path

from .band import Band
from .spectral_role import SpectralRole


class MultispectralBand(Band):
    def __init__(self, path: Path, index: int, resolution: tuple[float, float], role: SpectralRole) -> None:
        super().__init__(path, index, resolution)
        self._role = role

    def role(self) -> SpectralRole:
        return self._role
