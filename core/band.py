from pathlib import Path


class Band:
    def __init__(self, path: Path, index: int, resolution: tuple[float, float]) -> None:
        self._path = path
        self._index = index
        self._resolution = resolution

    def path(self) -> Path:
        return self._path

    def index(self) -> int:
        return self._index

    def resolution(self) -> tuple[float, float]:
        return self._resolution
