#!/usr/bin/env python3
"""
Главный модуль для трекера самолётов.
Пользователь может выбрать страну, получить топ N по высоте,
отфильтровать по стране регистрации и т.д.
"""

import logging
from typing import List

from src.aeroplane import Aeroplane
from src.plane_api import PlaneAPI
from src.json_storage import JSONSaver

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)


def get_top_n_aeroplanes(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    """Возвращает топ N самолётов по высоте полёта (от большего к меньшему)."""
    if not aeroplanes:
        return []
    # Сортируем по высоте (убывание)
    sorted_planes = sorted(aeroplanes, key=lambda p: p.baro_altitude, reverse=True)
    return sorted_planes[:top_n]


def filter_by_registration_country(aeroplanes: List[Aeroplane], countries: List[str]) -> List[Aeroplane]:
    """Фильтрует самолёты по списку стран регистрации (без учёта регистра)."""
    if not aeroplanes or not countries:
        return []
    countries_lower = [c.strip().lower() for c in countries]
    return [
        p for p in aeroplanes
        if p.origin_country and p.origin_country.lower() in countries_lower
    ]


def filter_by_altitude_range(aeroplanes: List[Aeroplane], min_alt: float, max_alt: float) -> List[Aeroplane]:
    """Фильтрует самолёты по диапазону высот."""
    if not aeroplanes:
        return []
    return [p for p in aeroplanes if min_alt <= p.baro_altitude <= max_alt]


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """Выводит список самолётов в консоль в удобочитаемом виде."""
    if not aeroplanes:
        print("❌ Самолёты не найдены.")
        return
    print(f"\n📋 Найдено самолётов: {len(aeroplanes)}\n")
    for i, plane in enumerate(aeroplanes, 1):
        print(f"{i}. {plane}")


def user_interaction() -> None:
    """Основной цикл взаимодействия с пользователем."""
    print("\n✈️  Добро пожаловать в трекер самолётов!")

    # 1. Ввод страны
    country = input("Введите название страны (например, 'France'): ").strip()
    if not country:
        print("❌ Страна не может быть пустой.")
        return

    # 2. Получение данных через API
    api = PlaneAPI()
    raw_planes = api.get_aeroplanes(country)
    if not raw_planes:
        print("❌ Не удалось получить данные о самолётах. Проверьте название страны или подключение к интернету.")
        return

    # 3. Преобразуем в список объектов Aeroplane
    aeroplanes = Aeroplane.cast_to_object_list(raw_planes.get("states", []))
    if not aeroplanes:
        print("❌ Нет данных о самолётах в указанном регионе.")
        return

    # 4. Сохраняем в JSON
    saver = JSONSaver("data/planes.json")
    saver.save_all(aeroplanes)
    print(f"💾 Данные сохранены в файл data/planes.json (всего {len(aeroplanes)} записей)")

    # 5. Основное меню
    while True:
        print("\n📌 Меню:")
        print("1. Показать топ N самолётов по высоте полёта")
        print("2. Фильтровать по стране регистрации")
        print("3. Фильтровать по диапазону высот")
        print("4. Показать все сохранённые самолёты (из файла)")
        print("5. Выйти")
        choice = input("Выберите действие (1-5): ").strip()

        if choice == "1":
            try:
                top_n = int(input("Введите количество N: "))
            except ValueError:
                print("❌ Введите целое число.")
                continue
            top_planes = get_top_n_aeroplanes(aeroplanes, top_n)
            print_aeroplanes(top_planes)

        elif choice == "2":
            countries_input = input("Введите страны регистрации через запятую (например, 'Russia, United States'): ")
            countries = [c.strip() for c in countries_input.split(",") if c.strip()]
            filtered = filter_by_registration_country(aeroplanes, countries)
            print_aeroplanes(filtered)

        elif choice == "3":
            try:
                min_alt = float(input("Минимальная высота (м): "))
                max_alt = float(input("Максимальная высота (м): "))
            except ValueError:
                print("❌ Введите корректные числа.")
                continue
            ranged = filter_by_altitude_range(aeroplanes, min_alt, max_alt)
            print_aeroplanes(ranged)

        elif choice == "4":
            all_saved = saver.load_all()
            print_aeroplanes(all_saved)

        elif choice == "5":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()