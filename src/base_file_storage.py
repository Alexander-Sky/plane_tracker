"""
Абстрактный базовый класс для работы с хранилищами данных.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.aeroplane import Aeroplane


class BaseFileStorage(ABC):
    """Абстрактный класс для работы с файловыми хранилищами."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes_by_country(self, country: str) -> List[Aeroplane]:
        """Возвращает список самолётов по стране регистрации."""
        pass

    @abstractmethod
    def get_aeroplanes_by_altitude(self, min_alt: float, max_alt: float) -> List[Aeroplane]:
        """Возвращает список самолётов в заданном диапазоне высот."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Удаляет самолёт из хранилища. Возвращает True, если удаление успешно."""
        pass

    @abstractmethod
    def load_all(self) -> List[Aeroplane]:
        """Загружает все сохранённые самолёты из хранилища."""
        pass

    @abstractmethod
    def save_all(self, aeroplanes: List[Aeroplane]) -> None:
        """Сохраняет список самолётов в хранилище (перезаписывает)."""
        pass