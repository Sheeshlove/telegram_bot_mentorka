import csv

# Путь к файлу с данными студентов
DATABASE_PATH = 'students_database.csv'

def check_full_name(fullname):
    """
    Проверяет наличие полного имени в базе данных
    Возвращает (True, данные_студента) если найдено, иначе (False, None)
    """
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['fullname'].lower() == fullname.lower():
                    return True, row
        return False, None
    except FileNotFoundError:
        print(f"Ошибка: файл {DATABASE_PATH} не найден")
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
        return (student_data.get('birth_date') == birth_date and 
                student_data.get('hometown').lower() == hometown.lower())
    return False

def verify_education_form(fullname, birth_date, hometown, education_form):
    """
    Проверяет соответствие формы обучения указанным данным студента
    """
    is_valid, student_data = check_full_name(fullname)
    if is_valid and student_data:
        return (student_data.get('birth_date') == birth_date and 
                student_data.get('hometown').lower() == hometown.lower() and
                student_data.get('education_form').lower() == education_form.lower())
    return False