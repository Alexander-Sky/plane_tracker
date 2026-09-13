"""
Класс для представления самолёта.
"""

from typing import Any, Dict, List, Optional


class Aeroplane:
    """Модель самолёта с валидацией и поддержкой сравнения."""

    def __init__(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        velocity: Optional[float],
        baro_altitude: Optional[float],
    ) -> None:
        """
        Инициализирует объект самолёта.

        Аргументы:
            icao24: уникальный идентификатор борта (строка).
            callsign: позывной рейса (строка).
            origin_country: страна регистрации самолёта.
            velocity: горизонтальная скорость (м/с), может быть None.
            baro_altitude: барометрическая высота (м), может быть None.
        """
        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else ""
        self.origin_country = origin_country
        self.velocity = self._validate_float(velocity, "velocity")
        self.baro_altitude = self._validate_float(baro_altitude, "baro_altitude")

    @staticmethod
    def _validate_float(value: Any, field_name: str) -> float:
        """Преобразует значение в float или возвращает 0.0 при невозможности."""
        if value is None:
            return 0.0
        try:
            return float(value)
        except TypeError, ValueError:
            return 0.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Aeroplane":
        """
        Создаёт объект Aeroplane из словаря, полученного от OpenSky API.

        Структура словаря (индексы):
        [0] icao24
        [1] callsign
        [2] origin_country
        [5] longitude (не используется для обязательных атрибутов)
        [6] latitude  (не используется)
        [7] baro_altitude
        [9] velocity
        """
        icao24 = data[0] if isinstance(data, list) and len(data) > 0 else ""
        callsign = data[1] if len(data) > 1 else ""
        origin_country = data[2] if len(data) > 2 else ""
        velocity = data[9] if len(data) > 9 else None
        baro_altitude = data[7] if len(data) > 7 else None

        return cls(icao24, callsign, origin_country, velocity, baro_altitude)

    @classmethod
    def cast_to_object_list(cls, raw_data: List[List[Any]]) -> List["Aeroplane"]:
        """Преобразует список списков от API в список объектов Aeroplane."""
        result = []
        for item in raw_data:
            if isinstance(item, list) and len(item) > 2:
                try:
                    result.append(cls.from_dict(item))
                except Exception as e:
                    # Логирование ошибки можно добавить позже
                    print(f"Ошибка при создании самолёта: {e}")
        return result

    def __repr__(self) -> str:
        return (
            f"Aeroplane(icao24={self.icao24}, callsign={self.callsign}, "
            f"origin_country={self.origin_country}, velocity={self.velocity}, "
            f"altitude={self.baro_altitude})"
        )

    def __str__(self) -> str:
        return (
            f"🛩️  {self.callsign or 'Без позывного'} | Страна: {self.origin_country} | "
            f"Скорость: {self.velocity:.1f} м/с | Высота: {self.baro_altitude:.1f} м"
        )

    # === Методы сравнения ===

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (
            self.velocity == other.velocity
            and self.baro_altitude == other.baro_altitude
        )

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости (для сортировки по возрастанию)."""
        return self.velocity < other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по скорости (для сортировки по убыванию)."""
        return self.velocity > other.velocity

    # Дополнительные методы для явного сравнения по высоте

    def is_higher_than(self, other: "Aeroplane") -> bool:
        """Сравнивает текущий самолёт с другим по высоте полёта."""
        return self.baro_altitude > other.baro_altitude

    def is_lower_than(self, other: "Aeroplane") -> bool:
        return self.baro_altitude < other.baro_altitude
