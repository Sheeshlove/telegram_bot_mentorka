import sqlite3
import csv
import os

# Путь к вашему файлу базы данных
DB_FILE = 'students.db'

# Проверяем, существует ли база данных
if not os.path.exists(DB_FILE):
    print("Ошибка: Файл базы данных не найден. Запустите сначала основное приложение.")
    exit(1)

# Путь к CSV файлу с данными студентов
csv_file = 'students.csv'  # Укажите свой путь, если он отличается

# Проверяем, существует ли CSV файл
if not os.path.exists(csv_file):
    print(f"Ошибка: Файл {csv_file} не найден.")
    exit(1)

# Подключаемся к базе данных
print("Подключение к базе данных...")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Чтение и загрузка данных из CSV
count = 0
try:
    print(f"Чтение данных из файла {csv_file}...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        
        # Проверяем первую строку - это может быть заголовок
        first_row = next(csv_reader)
        if first_row[0].lower() != 'иванов' and 'фио' in first_row[0].lower():
            print("Обнаружен заголовок, пропускаем первую строку.")
        else:
            # Если первая строка не заголовок, а данные, добавляем её
            cursor.execute('''
            INSERT INTO students (full_name, birth_date, hometown, education_form)
            VALUES (?, ?, ?, ?)
            ''', (first_row[0], first_row[1], first_row[2], first_row[3]))
            count += 1
        
        # Обрабатываем остальные строки
        for row in csv_reader:
            if len(row) >= 4:  # Проверяем, что строка содержит все необходимые данные
                full_name, birth_date, hometown, education_form = row[0], row[1], row[2], row[3]
                
                # Пропускаем строки с пустым ФИО
                if not full_name.strip():
                    continue
                
                # Добавляем данные в базу
                cursor.execute('''
                INSERT INTO students (full_name, birth_date, hometown, education_form)
                VALUES (?, ?, ?, ?)
                ''', (full_name, birth_date, hometown, education_form))
                
                count += 1
            else:
                print(f"Предупреждение: строка {count+1} содержит неполные данные, пропускаем.")

    # Сохраняем изменения
    conn.commit()
    print(f"Успешно добавлено {count} студентов из CSV файла в базу данных.")

except Exception as e:
    print(f"Произошла ошибка при импорте данных: {e}")
    conn.rollback()  # Отменяем все изменения в случае ошибки

finally:
    # Закрываем соединение с базой данных
    conn.close()
    print("Соединение с базой данных закрыто.")

# Вывод информации о проверке
print("\nДля проверки импортированных данных запустите скрипт:")
print("from database import get_all_students")
print("students = get_all_students()")
print("for student in students:")
print("    print(student)")