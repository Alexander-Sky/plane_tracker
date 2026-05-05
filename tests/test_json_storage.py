import os
import tempfile
import pytest
from src.json_storage import JSONSaver
from src.aeroplane import Aeroplane


@pytest.fixture
def temp_storage():
    """Создаёт временный файл для тестов."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        storage = JSONSaver(f.name)
    yield storage
    os.unlink(f.name)


def test_add_and_load_all(temp_storage):
    """Тест добавления и загрузки самолётов."""
    plane = Aeroplane("abc123", "SU123", "Russia", 250.5, 10000.0)
    temp_storage.add_aeroplane(plane)
    loaded = temp_storage.load_all()
    assert len(loaded) == 1
    assert loaded[0].icao24 == "abc123"


def test_delete_aeroplane(temp_storage):
    """Тест удаления самолёта."""
    plane = Aeroplane("abc123", "SU123", "Russia", 250.5, 10000.0)
    temp_storage.add_aeroplane(plane)
    assert temp_storage.delete_aeroplane(plane) is True
    assert len(temp_storage.load_all()) == 0


def test_get_by_country(temp_storage):
    """Тест поиска по стране регистрации."""
    plane1 = Aeroplane("a", "A1", "Russia", 200.0, 10000.0)
    plane2 = Aeroplane("b", "B2", "USA", 220.0, 11000.0)
    temp_storage.add_aeroplane(plane1)
    temp_storage.add_aeroplane(plane2)
    result = temp_storage.get_aeroplanes_by_country("Russia")
    assert len(result) == 1
    assert result[0].origin_country == "Russia"