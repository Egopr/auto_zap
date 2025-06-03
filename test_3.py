import csv
import os
from typing import List, Dict, Optional

CSV_FILE = "data.csv"
FIELDNAMES = ["name", "age", "email"]


def init_csv(file_path: str = CSV_FILE):
    """Создаёт CSV-файл с заголовками, если его нет."""
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def add_data(name: str, age: int, email: str, file_path: str = CSV_FILE):
    """Добавляет новую запись в CSV."""
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({"name": name, "age": age, "email": email})
    print(f"✅ Данные добавлены: {name}, {age}, {email}")


def get_all_data(file_path: str = CSV_FILE) -> List[Dict[str, str]]:
    """Возвращает все данные из CSV."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def search_data(query: str, field: str = "name", file_path: str = CSV_FILE) -> List[Dict[str, str]]:
    """Ищет данные по заданному полю."""
    if field not in FIELDNAMES:
        return []

    results = []
    with open(file_path, mode="r", encoding="utf-8") as file:
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


def load_new_file():
    """Загружает новый CSV-файл для работы."""
    global CSV_FILE
    new_file = input("Введите путь к новому CSV-файлу: ").strip()

    if not new_file.endswith('.csv'):
        new_file += '.csv'

    if os.path.exists(new_file):
        # Проверяем, есть ли нужные заголовки в файле
        with open(new_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames and all(field in reader.fieldnames for field in FIELDNAMES):
                CSV_FILE = new_file
                print(f"✅ Файл {new_file} успешно загружен!")
            else:
                print("❌ Файл не содержит необходимых столбцов (name, age, email).")
    else:
        print("❌ Файл не найден. Создать новый? (y/n)")
        choice = input().lower()
        if choice == 'y':
            CSV_FILE = new_file
            init_csv()
            print(f"✅ Создан новый файл {new_file}")
        else:
            print("❌ Отмена загрузки файла.")


def main():
    init_csv()  # Инициализация файла

    while True:
        print("\n📋 Меню:")
        print("1. Добавить данные")
        print("2. Найти данные")
        print("3. Показать все данные")
        print("4. Загрузить другой CSV-файл")
        print("5. Выход")

        choice = input("Выберите действие (1-5): ")

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
            load_new_file()

        elif choice == "5":
            print("Выход...")
            break

        else:
            print("❌ Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()