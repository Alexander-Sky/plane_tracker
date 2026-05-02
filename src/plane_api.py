import logging
from typing import List, Dict, Any

import requests

from src.base_api import BaseAPI

logger = logging.getLogger(__name__)


class PlaneAPI(BaseAPI):
    """Класс для получения данных о самолётах через OpenSky и координат стран через Nominatim."""

    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Получить список самолётов для указанной страны.

        Шаги:
        1. Запрашиваем у Nominatim географические границы страны (boundingbox).
        2. Передаём границы в OpenSky и получаем список самолётов.

        Аргументы:
            country: название страны (например, 'France').

        Возвращает:
            Список словарей с данными самолётов (каждый элемент — одна запись из OpenSky).
        """
        logger.info(f"Запрос данных для страны: {country}")

        # 1. Получаем границы страны
        geo_coords = self._get_country_bounds(country)
        if not geo_coords:
            logger.error(f"Не удалось получить координаты для страны '{country}'")
            return []

        # 2. Запрашиваем самолёты в этих границах
        aeroplanes_response = self._fetch_planes_in_bbox(geo_coords)
        if not aeroplanes_response:
            logger.error("Не удалось получить данные от OpenSky")
            return []

        # 3. Извлекаем список самолётов
        states = aeroplanes_response.get("states")
        if not isinstance(states, list):
            logger.warning(f"Поле 'states' отсутствует или имеет неверный тип: {type(states)}")
            return []

        logger.info(f"Найдено {len(states)} самолётов над {country}")
        return states

    def _get_country_bounds(self, country: str) -> List[str]:
        """
        Запрашивает границы страны у Nominatim и возвращает boundingbox.
        """
        headers = {"User-Agent": "plane-tracker-app/1.0"}
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response = requests.get(
                self.openstreetmap_url,
                headers=headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к Nominatim: {e}")
            return []

        if not data or not isinstance(data, list):
            logger.warning(f"Некорректный ответ от Nominatim: {data}")
            return []

        bounding_box = data[0].get("boundingbox")
        if not bounding_box or len(bounding_box) != 4:
            logger.warning(f"boundingbox отсутствует или имеет неверный формат: {bounding_box}")
            return []

        logger.debug(f"Координаты для {country}: {bounding_box}")
        return bounding_box

    def _fetch_planes_in_bbox(self, bbox: List[str]) -> Dict[str, Any]:
        """
        Запрашивает данные OpenSky для заданного bounding box.
        bbox = [южная широта, северная широта, западная долгота, восточная долгота]
        """
        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3],
        }

        try:
            response = requests.get(self.opensky_url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к OpenSky: {e}")
            return {}