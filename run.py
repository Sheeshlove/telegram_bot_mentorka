import os
import importlib
import time
from bot_init import bot

# Загрузка всех модулей проекта
def load_modules():
    modules = []
    excluded_files = ['run.py', '__init__.py', 'bot_init.py', 'user_management.py', 'snippet.py']
    
    for file in os.listdir():
        if file.endswith('.py') and file not in excluded_files:
            module_name = file[:-3]  # Убираем расширение .py
            try:
                module = importlib.import_module(module_name)
                modules.append(module)
                print(f"✅ Модуль '{module_name}' успешно загружен")
            except Exception as e:
                print(f"❌ Ошибка загрузки модуля '{module_name}': {e}")
    return modules

# Инициализация и запуск бота
def run_bot():
    print("🤖 Запуск бота...")

    # Загружаем модули
    modules = load_modules()

    # Запускаем бот в бесконечном цикле с обработкой ошибок
    while True:
        try:
            # Удаляем webhook перед запуском polling
            bot.remove_webhook()
            print("✅ Webhook удален")

            # Запускаем бот
            print("✅ Бот запущен и прослушивает сообщения")
            bot.polling(none_stop=True, interval=0, timeout=60)

        except Exception as e:
            print(f"❌ Ошибка при работе бота: {e}")
            # Ждем перед повторным запуском
            time.sleep(15)
            print("🔄 Перезапуск бота...")

if __name__ == "__main__":
    run_bot()