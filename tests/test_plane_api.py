from unittest.mock import patch

from src.plane_api import PlaneAPI


@patch("src.plane_api.requests.get")
def test_get_aeroplanes_success(mock_get):
    """Тест успешного получения данных самолётов."""
    # Мокаем ответ Nominatim
    mock_get.side_effect = [
        MockResponse([{"boundingbox": ["40", "50", "-10", "10"]}], 200),
        MockResponse(
            {"states": [["a", "b", "c", None, None, None, None, 10000.0, None, 200.0]]},
            200,
        ),
    ]
    api = PlaneAPI()
    result = api.get_aeroplanes("Spain")
    assert len(result) == 1
    assert result[0][1] == "b"  # callsign на позиции 1


@patch("src.plane_api.requests.get")
def test_get_aeroplanes_no_country(mock_get):
    """Тест: страна не найдена."""
    mock_get.return_value = MockResponse([], 200)
    api = PlaneAPI()
    result = api.get_aeroplanes("Nowhereland")
    assert result == []


class MockResponse:
    """Заглушка для ответа requests."""

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP Error")
