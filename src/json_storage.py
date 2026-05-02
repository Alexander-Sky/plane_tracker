"""
Реализация хранилища в JSON-файле.
"""

import json
from typing import List, Optional

from src.aeroplane import Aeroplane
from src.base_file_storage import BaseFileStorage


class JSONSaver(BaseFileStorage):
    """Класс для сохранения данных о самолётах в JSON-файл."""

    def __init__(self, filename: str = "data/planes.json"):
        """
        Инициализирует хранилище.

        Args:
            filename: Путь к JSON-файлу для хранения данных.
        """
        self.filename = filename

    def _load_from_file(self) -> List[dict]:
        """Загружает данные из JSON-файла. Если файл не существует или пуст — возвращает пустой список."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self, data: List[dict]) -> None:
        """Сохраняет данные в JSON-файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в файл."""
        data = self._load_from_file()

        # Проверяем, есть ли уже такой самолёт (по icao24)
        for item in data:
            if item.get('icao24') == aeroplane.icao24:
                return  # уже существует

        data.append({
            'icao24': aeroplane.icao24,
            'callsign': aeroplane.callsign,
            'origin_country': aeroplane.origin_country,
            'velocity': aeroplane.velocity,
            'baro_altitude': aeroplane.baro_altitude,
        })
        self._save_to_file(data)

    def get_aeroplanes_by_country(self, country: str) -> List[Aeroplane]:
        """Возвращает список самолётов по стране регистрации."""
        data = self._load_from_file()
        result = []
        for item in data:
            if item.get('origin_country', '').lower() == country.lower():
                try:
                    aeroplane = Aeroplane(
                        icao24=item.get('icao24', ''),
                        callsign=item.get('callsign', ''),
                        origin_country=item.get('origin_country', ''),
                        velocity=item.get('velocity'),
                        baro_altitude=item.get('baro_altitude'),
                    )
                    result.append(aeroplane)
                except Exception:
                    continue
        return result

    def get_aeroplanes_by_altitude(self, min_alt: float, max_alt: float) -> List[Aeroplane]:
        """Возвращает список самолётов в заданном диапазоне высот."""
        data = self._load_from_file()
        result = []
        for item in data:
            alt = item.get('baro_altitude')
            if alt is not None and min_alt <= alt <= max_alt:
                try:
                    aeroplane = Aeroplane(
                        icao24=item.get('icao24', ''),
                        callsign=item.get('callsign', ''),
                        origin_country=item.get('origin_country', ''),
                        velocity=item.get('velocity'),
                        baro_altitude=alt,
                    )
                    result.append(aeroplane)
                except Exception:
                    continue
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Удаляет самолёт из файла. Возвращает True, если удаление успешно."""
        data = self._load_from_file()
        initial_len = len(data)
        new_data = [item for item in data if item.get('icao24') != aeroplane.icao24]
        if len(new_data) < initial_len:
            self._save_to_file(new_data)
            return True
        return False

    def load_all(self) -> List[Aeroplane]:
        """Загружает все сохранённые самолёты."""
        data = self._load_from_file()
        result = []
        for item in data:
            try:
                aeroplane = Aeroplane(
                    icao24=item.get('icao24', ''),
                    callsign=item.get('callsign', ''),
                    origin_country=item.get('origin_country', ''),
                    velocity=item.get('velocity'),
                    baro_altitude=item.get('baro_altitude'),
                )
                result.append(aeroplane)
            except Exception:
                continue
        return result

    def save_all(self, aeroplanes: List[Aeroplane]) -> None:
        """Перезаписывает файл новым списком самолётов."""
        data = []
        for a in aeroplanes:
            data.append({
                'icao24': a.icao24,
                'callsign': a.callsign,
                'origin_country': a.origin_country,
                'velocity': a.velocity,
                'baro_altitude': a.baro_altitude,
            })
        self._save_to_file(data)