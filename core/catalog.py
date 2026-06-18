from core.bands import SpectralBand


class SpectralCatalog:
    def all_bands(self) -> list[SpectralBand]:
        ...

    def nearest_band(
        self,
        wavelength_nm: float
    ) -> SpectralBand:
        ...
