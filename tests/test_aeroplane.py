import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    """Тест создания объекта Aeroplane."""
    plane = Aeroplane("abc123", "SU123", "Russia", 250.5, 10000.0)
    assert plane.icao24 == "abc123"
    assert plane.callsign == "SU123"
    assert plane.origin_country == "Russia"
    assert plane.velocity == 250.5
    assert plane.baro_altitude == 10000.0


def test_aeroplane_invalid_velocity():
    """Тест обработки невалидной скорости."""
    plane = Aeroplane("abc123", "SU123", "Russia", None, 10000.0)
    assert plane.velocity == 0.0


def test_aeroplane_comparison():
    """Тест сравнения самолётов по скорости."""
    plane1 = Aeroplane("a", "A", "Rus", 100.0, 5000.0)
    plane2 = Aeroplane("b", "B", "Rus", 200.0, 6000.0)

    assert plane1 < plane2
    assert plane2 > plane1
    assert plane1 != plane2


def test_aeroplane_from_dict():
    """Тест создания объекта из словаря от API."""
    data = ["abc123", "SU123", "Russia", None, None, None, None, 10000.0, None, 250.5]
    plane = Aeroplane.from_dict(data)
    assert plane.icao24 == "abc123"
    assert plane.callsign == "SU123"
    assert plane.origin_country == "Russia"
    assert plane.velocity == 250.5
    assert plane.baro_altitude == 10000.0


def test_cast_to_object_list():
    """Тест преобразования списка от API в список объектов."""
    raw_data = [
        ["a", "A1", "Russia", None, None, None, None, 10000.0, None, 200.0],
        ["b", "B2", "USA", None, None, None, None, 11000.0, None, 220.0],
        ["c", "C3", "Germany", None, None, None, None, 12000.0, None, 240.0],
    ]
    planes = Aeroplane.cast_to_object_list(raw_data)
    assert len(planes) == 3
    assert isinstance(planes[0], Aeroplane)