from core.exceptions import UnsupportedProductError


class ProviderRegistry:
    _providers = []

    @classmethod
    def register(cls, provider):
        cls._providers.append(provider)

    @classmethod
    def open(cls, path):
        for provider in cls._providers:
            if provider.can_open(path):
                return provider.open(path)

        raise UnsupportedProductError()
