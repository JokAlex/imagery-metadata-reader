from abc import abstractmethod

from .multispectral_band import MultispectralBand
from .spectral_product import SpectralProduct
from .spectral_role import SpectralRole


class MultispectralProduct(SpectralProduct):
    @abstractmethod
    def band_by_role(self, role: SpectralRole) -> MultispectralBand:
        ...
