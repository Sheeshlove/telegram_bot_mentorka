import os
import importlib
import telebot
from telebot import types


# Загрузка всех модулей проекта
def load_modules():
    modules = []
    for file in os.listdir():
        if file.endswith('.py') and file != 'run.py' and file != '__init__.py':
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

    # Получаем объект бота из первого модуля, где он определен
    bot = None
    for module in modules:
        if hasattr(module, 'bot'):
            bot = module.bot
            break

    if not bot:
        print("❌ Объект бота не найден ни в одном из модулей!")
        return

    # Запускаем бот
    print("✅ Бот запущен и прослушивает сообщения")
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    run_bot()

try:
    # Добавляем параметр none_stop=True чтобы бот не останавливался при возникновении ошибок
    # Добавляем параметр timeout=123 чтобы установить время ожидания запроса
    # Добавляем параметр allowed_updates=[] чтобы указать типы обновлений, которые будут обрабатываться
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.polling(none_stop=True, interval=0, timeout=20)
except Exception as e:
    print(f"Произошла ошибка: {e}")
    # Ждем 15 секунд перед повторным запуском
    import time

    time.sleep(15)
