import csv
import os

# Путь к файлу с данными студентов
DATABASE_PATH = 'students_database.csv'

def check_full_name(fullname):
    """
    Проверяет наличие полного имени в базе данных
    Возвращает (True, данные_студента) если найдено, иначе (False, None)
    """
    try:
        if not os.path.exists(DATABASE_PATH):
            print(f"Ошибка: файл {DATABASE_PATH} не найден")
            return False, None
            
        with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['full_name'].lower() == fullname.lower():
                    return True, row
        return False, None
    except Exception as e:
        print(f"Ошибка при чтении файла БД: {e}")
        return False, None

def verify_birth_date(fullname, birth_date):
    """
    Проверяет соответствие даты рождения указанному имени
    """
    is_valid, student_data = check_full_name(fullname)
    if is_valid and student_data:
        return student_data.get('birth_date') == birth_date
    return False

def verify_hometown(fullname, birth_date, hometown):
    """
    Проверяет соответствие города рождения указанному имени и дате рождения
    """
    is_valid, student_data = check_full_name(fullname)
    if is_valid and student_data:
        # Проверяем совпадение даты рождения и города
        return (student_data.get('birth_date') == birth_date and 
                student_data.get('hometown', '').lower() == hometown.lower())
    return False

def verify_education_form(fullname, birth_date, hometown, education_form):
    """
    Проверяет соответствие формы обучения указанным данным студента
    """
    is_valid, student_data = check_full_name(fullname)
    if is_valid and student_data:
        # Проверяем совпадение всех полей
        return (student_data.get('birth_date') == birth_date and 
                student_data.get('hometown', '').lower() == hometown.lower() and
                student_data.get('education_form', '').lower() == education_form.lower())
    return False

def get_all_students():
    """Возвращает список всех студентов"""
    students = []
    try:
        if not os.path.exists(DATABASE_PATH):
            return students
            
        with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
        return students
    except Exception as e:
        print(f"Ошибка при получении списка студентов: {e}")
        return []