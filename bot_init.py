import telebot

# Токен вашего бота
TOKEN = '7223734470:AAFOmEA7pVKS0YZTLS0dt-6HQAPJWTLvHnU'

# Инициализация бота
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ID канала
CHANNEL_ID = -1002573117796