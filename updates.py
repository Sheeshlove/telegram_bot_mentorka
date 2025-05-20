import telebot
from telebot import types

# Токен вашего бота
TOKEN = '7223734470:AAFOmEA7pVKS0YZTLS0dt-6HQAPJWTLvHnU'
CHANNEL_ID = -1002573117796  # Числовой ID канала (не @username)
USER_ID = @sheeshlove  # Замените на ваш реальный ID

bot = telebot.TeleBot(TOKEN)

# Отладка получения обновлений
@bot.channel_post_handler(content_types=['text', 'photo', 'video', 'document', 'audio'])
def handle_channel_posts(message):
    print(f"Получено сообщение из канала: {message.chat.id}")
    try:
        # Пересылаем сообщение в личный чат пользователя
        bot.forward_message(USER_ID, message.chat.id, message.message_id)
        print(f"Сообщение переслано пользователю {USER_ID}")
    except Exception as e:
        print(f"Ошибка при пересылке: {e}")