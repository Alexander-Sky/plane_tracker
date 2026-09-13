from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list:
        """Получить список самолётов в воздушном пространстве страны."""
        pass
