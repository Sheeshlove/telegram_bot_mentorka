import sqlite3
import os

# Путь к файлу базы данных
DB_FILE = 'students.db'

def init_db():
    """Инициализирует базу данных и создает таблицу, если она не существует"""
    # Проверяем, существует ли файл базы данных
    db_exists = os.path.exists(DB_FILE)
    
    # Подключаемся к базе данных (или создаем новую, если она не существует)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        hometown TEXT,
        education_form TEXT
    )
    ''')
    
    # Если база данных только что создана, добавляем тестовые данные
    if not db_exists:
        # Вставляем тестовые данные
        test_data = [
            ('Иванов Иван Иванович', '09-05-2004', None, None),
            ('Александров Александр Александрович', '01-01-2007', 'Москва', 'Бюджетная')
        ]
        cursor.executemany('''
        INSERT INTO students (full_name, birth_date, hometown, education_form)
        VALUES (?, ?, ?, ?)
        ''', test_data)
    
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

# Инициализируем базу данных при импорте модуля
init_db()

def check_full_name(name):
    """Проверяет наличие студента с указанным ФИО в базе данных"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Ищем студента по ФИО
    cursor.execute('SELECT * FROM students WHERE full_name = ?', (name,))
    student = cursor.fetchone()
    
    conn.close()
    
    if student:
        # Конвертируем результат в словарь
        student_dict = {
            'full_name': student[1],
            'birth_date': student[2],
            'hometown': student[3],
            'education_form': student[4]
        }
        return True, student_dict
    
    return False, None

def verify_birth_date(name, birth_date):
    """Проверяет соответствие даты рождения для указанного студента"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Ищем студента по ФИО и дате рождения
    cursor.execute('SELECT * FROM students WHERE full_name = ? AND birth_date = ?', 
                  (name, birth_date))
    student = cursor.fetchone()
    
    conn.close()
    
    return student is not None

def verify_hometown(name, birth_date, hometown):
    """Проверяет соответствие родного города для указанного студента"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Ищем студента по ФИО, дате рождения и городу
    cursor.execute('''
    SELECT * FROM students 
    WHERE full_name = ? AND birth_date = ? AND hometown = ?
    ''', (name, birth_date, hometown))
    student = cursor.fetchone()
    
    conn.close()
    
    return student is not None

def verify_education_form(name, birth_date, hometown, education_form):
    """Проверяет соответствие формы обучения для указанного студента"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Ищем студента по всем параметрам
    cursor.execute('''
    SELECT * FROM students 
    WHERE full_name = ? AND birth_date = ? AND hometown = ? AND education_form = ?
    ''', (name, birth_date, hometown, education_form))
    student = cursor.fetchone()
    
    conn.close()
    
    return student is not None

def add_student(full_name, birth_date, hometown=None, education_form=None):
    """Добавляет нового студента в базу данных"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO students (full_name, birth_date, hometown, education_form)
    VALUES (?, ?, ?, ?)
    ''', (full_name, birth_date, hometown, education_form))
    
    conn.commit()
    conn.close()
    
    return True

def get_all_students():
    """Возвращает список всех студентов"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students')
    students_raw = cursor.fetchall()
    
    conn.close()
    
    # Преобразуем результаты в список словарей
    students = []
    for student in students_raw:
        students.append({
            'id': student[0],
            'full_name': student[1],
            'birth_date': student[2],
            'hometown': student[3],
            'education_form': student[4]
        })
    
    return students