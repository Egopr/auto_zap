import csv
import os
from typing import List, Dict, Optional

CSV_FILE = "data.csv"
FIELDNAMES = ["name", "age", "email"]


def init_csv():
    """Создаёт CSV-файл с заголовками, если его нет."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def add_data(name: str, age: int, email: str):
    """Добавляет новую запись в CSV."""
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({"name": name, "age": age, "email": email})
    print(f"✅ Данные добавлены: {name}, {age}, {email}")


def get_all_data() -> List[Dict[str, str]]:
    """Возвращает все данные из CSV."""
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def search_data(query: str, field: str = "name") -> List[Dict[str, str]]:
    """Ищет данные по заданному полю."""
    if field not in FIELDNAMES:
        return []

    results = []
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if query.lower() in row[field].lower():
                results.append(row)
    return results


def print_data(data: List[Dict[str, str]]):
    """Выводит данные в читаемом формате."""
    if not data:
        print("❌ Данные не найдены.")
        return

    for idx, row in enumerate(data, 1):
        print(f"{idx}. Имя: {row['name']}, Возраст: {row['age']}, Email: {row['email']}")


def main():
    init_csv()  # Инициализация файла

    while True:
        print("\n📋 Меню:")
        print("1. Добавить данные")
        print("2. Найти данные")
        print("3. Показать все данные")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            name = input("Имя: ")
            age = input("Возраст: ")
            email = input("Email: ")
            add_data(name, age, email)

        elif choice == "2":
            field = input("Поиск по (name/age/email): ").strip().lower()
            query = input("Введите запрос: ")
            results = search_data(query, field)
            print_data(results)

        elif choice == "3":
            data = get_all_data()
            print_data(data)

        elif choice == "4":
            print("Выход...")
            break

        else:
            print("❌ Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()