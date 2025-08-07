import os

# Файл для хранения ID пользователей
USERS_FILE = 'users.txt'

def add_user(user_id):
    """
    Добавляет ID пользователя в файл, если он еще не существует
    """
    try:
        # Создаем файл, если он не существует
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w') as f:
                f.write('')
        
        # Читаем существующих пользователей
        with open(USERS_FILE, 'r') as f:
            users = [int(line.strip()) for line in f if line.strip().isdigit()]
        
        # Добавляем нового пользователя
        if user_id not in users:
            with open(USERS_FILE, 'a') as f:
                f.write(f"{user_id}\n")
            return True
        return False
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False

def get_all_users():
    """
    Возвращает список всех ID пользователей из файла
    """
    try:
        if not os.path.exists(USERS_FILE):
            return []
            
        with open(USERS_FILE, 'r') as f:
            users = [int(line.strip()) for line in f if line.strip().isdigit()]
        return users
    except Exception as e:
        print(f"Ошибка при получении списка пользователей: {e}")
        return []

def remove_user(user_id):
    """
    Удаляет ID пользователя из файла
    """
    try:
        # Получаем список пользователей
        users = get_all_users()
        
        if user_id in users:
            # Удаляем пользователя из списка
            users.remove(user_id)
            
            # Записываем обновленный список обратно в файл
            with open(USERS_FILE, 'w') as f:
                for uid in users:
                    f.write(f"{uid}\n")
            return True
        return False
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
        return False
