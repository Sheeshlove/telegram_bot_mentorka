from bot_init import bot, CHANNEL_ID
from telebot import types
import user_management

# Обработчик команды подписки на обновления
@bot.message_handler(commands=['subscribe'])
def subscribe_to_updates(message):
    user_id = message.from_user.id
    if user_management.add_user(user_id):
        bot.send_message(message.chat.id, "Вы успешно подписались на обновления канала!")
    else:
        bot.send_message(message.chat.id, "Вы уже подписаны на обновления.")

# Обработчик команды отписки от обновлений
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe_from_updates(message):
    user_id = message.from_user.id
    if user_management.remove_user(user_id):
        bot.send_message(message.chat.id, "Вы успешно отписались от обновлений!")
    else:
        bot.send_message(message.chat.id, "Вы не были подписаны на обновления.")

# Функция для пересылки сообщений из канала всем подписчикам
def forward_channel_updates(message):
    # Проверяем, что сообщение пришло из нужного канала
    if message.chat.id == CHANNEL_ID:
        # Получаем список подписчиков
        users = user_management.get_all_users()
        
        # Пересылаем сообщение каждому подписчику
        for user_id in users:
            try:
                # Пересылаем сообщение пользователю
                bot.forward_message(user_id, CHANNEL_ID, message.message_id)
            except Exception as e:
                print(f"Ошибка при пересылке сообщения пользователю {user_id}: {e}")

# Регистрируем обработчик для всех типов сообщений из канала
@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    forward_channel_updates(message)