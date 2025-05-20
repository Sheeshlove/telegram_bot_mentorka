import random

import telebot
from telebot import types

from database import check_full_name, verify_birth_date, verify_hometown, verify_education_form

bot = telebot.TeleBot('7223734470:AAFOmEA7pVKS0YZTLS0dt-6HQAPJWTLvHnU')

mentors = ["@sheeshlove", "@correttoo", "@viuklllaaa"]

# Словарь для отслеживания состояния пользователей и их данных
user_states = {}
user_data = {}  # Отдельный словарь для хранения данных пользователей
AWAITING_NAME = "awaiting_name"
AWAITING_BIRTH_DATE = "awaiting_birth_date"
AWAITING_HOMETOWN = 'awaiting_hometown'
AWAITING_EDUCATION_FORM = 'awaiting_education_form'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\n"
                                      f"\n"
                                      f"Я бот менторской программы ФМО, пытаться со мной говорить бесплезно, однако я всё ещё могу тебе помочь! Вот команды, с которыми я работаю:\n"
                                      f"\n"
                                      f"<b>/mentor</b> - я дам тебе ссылку на одного из представителей программы, кто ответит на твои вопросы\n"
                                      f"\n"
                                      f"<b>/links</b> - я дам тебе ссылки на все самые важные ресурсы для любого международника\n"
                                      f"\n"
                                      f"<b>/chat</b> - я дам тебе ссылку на чат твоего потока. \n"
                                      f"<b>Важно! Беседа появится не раньше 15 августа, потому что мы ждём, когда появятся списки всех поступивших</b>\n"
                                      f"\n"
                                      f"<b>/pamatka</b> - я дам тебе ссылку на священный грааль - памятку первокурсника",
                     parse_mode='html')


@bot.message_handler(commands=['pamatka'])
def start(message):
    pamatka = types.InlineKeyboardMarkup()
    pamatka.add(types.InlineKeyboardButton('Почитать памятку', url='https://disk.yandex.ru/d/XElmsMv8yYqVZg'))
    bot.send_message(message.chat.id,
                     f'Это - памятка первокурсника. Мы подготовили её для тебя, чтобы тебе было прохе освоиться на нашем факультете. Тут собраны ответы на все самые острые вопросы, которые могут у тебя возникуть. Почаще обращайся к ней!',
                     reply_markup=pamatka)


@bot.message_handler(commands=['mentor'])
def mentor_command(message):
    random_mentor = random.choice(mentors)
    mentor = types.InlineKeyboardMarkup()
    mentor.add(types.InlineKeyboardButton('Смотреть памятку', url='https://disk.yandex.ru/d/XElmsMv8yYqVZg'))
    bot.send_message(message.chat.id, f"твой супергерой сегодня - {random_mentor}!\n"
                                      "\n"
                                      f"Пожалуйста, помни, что ментор может не всегда быть на связи, особенно, если ты пишешь посреди ночи.\n"
                                      f"\n"
                                      f"Прежде чем писать ментору, проверь, нет ли ответа на твой вопрос в [памятке первокурсника](https://disk.yandex.ru/d/XElmsMv8yYqVZg)",
                     parse_mode='Markdown', reply_markup=mentor)


@bot.message_handler(commands=['links'])
def links_command(message):
    bot.send_message(message.chat.id, "Ресурсы менторской программы:\n"
                                      "ТГК: https://t.me/mentorkafmo \n"
                                      "ВК: https://vk.com/mentorka_fmo\n"
                                      "\n"
                                      "<b>Студенческий Совет</b>:\n"
                                      "ФМО https://vk.com/sirspbu\n"
                                      "СПбГУ https://vk.com/ssspbu\n "
                                      "\n"
                                      "<b>Прочие каналы</b>:\n "
                                      "Студенческое Научное Общество - https://vk.com/snofmo\n"
                                      "Смольный Знает (ВК) - https://vk.com/smolnyknows\n "
                                      "Смольный Знает (ТГ) - https://t.me/smolnyknows\n "
                                      "Клуб Молодёжной Дипломатии - https://t.me/dipclub_spbu\n"
                                      "Смольный Флекс - https://vk.com/smolnyflex", parse_mode='html')


@bot.message_handler(commands=['chat'])
def chat_command(message):
    user_id = message.from_user.id
    user_states[user_id] = AWAITING_NAME
    user_data[user_id] = {}  # Инициализируем пустой словарь для данных пользователя
    bot.send_message(message.chat.id,
                     "Чтобы попасть в чат, тебе нужно пройти небольшую проверку. Это сделано, чтобы в чате могли оказаться только настоящие первокурсники. Пожалуйста, напиши своё ФИО как в паспорте.")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_NAME)
def check_fullname(message):
    user_id = message.from_user.id
    fullname = message.text.strip()

    is_valid, student_data = check_full_name(fullname)

    if is_valid:
        # Сохраняем ФИО и переходим к следующему этапу
        user_data[user_id]["fullname"] = fullname
        user_states[user_id] = AWAITING_BIRTH_DATE
        bot.send_message(message.chat.id, "Напишите свою дату рождения в формате ДД-ММ-ГГГГ")
    else:
        # Удаляем состояние пользователя
        if user_id in user_states:
            user_states.pop(user_id)
        if user_id in user_data:
            user_data.pop(user_id)
        random_mentor = random.choice(mentors)
        bot.send_message(message.chat.id,
                         f"К сожалению, вас нет в списках на поступление. Если вам кажется, что произошла ошибка, пожалуйста, свяжитесь с кем-то из менторов, например с {random_mentor}")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_BIRTH_DATE)
def check_birth_date(message):
    user_id = message.from_user.id
    birth_date = message.text.strip()

    if user_id in user_data:
        fullname = user_data[user_id].get("fullname", "")

        if verify_birth_date(fullname, birth_date):
            # Сохраняем дату рождения и переходим к запросу города
            user_data[user_id]["birth_date"] = birth_date
            user_states[user_id] = AWAITING_HOMETOWN
            bot.send_message(message.chat.id, "Пожалуйста, введите свой город рождения (как в паспорте)")
        else:
            # Удаляем состояние пользователя
            if user_id in user_states:
                user_states.pop(user_id)
            if user_id in user_data:
                user_data.pop(user_id)

            random_mentor = random.choice(mentors)
            bot.send_message(message.chat.id,
                             f"К сожалению, данные не совпадают с нашими записями. Если вам кажется, что произошла ошибка, пожалуйста, свяжитесь с кем-то из менторов, например с {random_mentor}")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, начните процесс заново с команды /chat")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_HOMETOWN)
def check_hometown(message):
    user_id = message.from_user.id
    hometown = message.text.strip()

    if user_id in user_data:
        fullname = user_data[user_id].get("fullname", "")
        birth_date = user_data[user_id].get("birth_date", "")

        if verify_hometown(fullname, birth_date, hometown):
            # Сохраняем город и переходим к запросу формы обучения
            user_data[user_id]["hometown"] = hometown
            user_states[user_id] = AWAITING_EDUCATION_FORM

            # Создаем клавиатуру с кнопками для выбора формы обучения
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton('Бюджетная')
            btn2 = types.KeyboardButton('Договорная')
            markup.add(btn1, btn2)

            bot.send_message(message.chat.id, "Пожалуйста, укажите форму вашего обучения:", reply_markup=markup)
        else:
            # Удаляем состояние пользователя
            if user_id in user_states:
                user_states.pop(user_id)
            if user_id in user_data:
                user_data.pop(user_id)

            random_mentor = random.choice(mentors)
            bot.send_message(message.chat.id,
                             f"К сожалению, данные не совпадают с нашими записями. Если вам кажется, что произошла ошибка, пожалуйста, свяжитесь с кем-то из менторов, например с {random_mentor}")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, начните процесс заново с команды /chat")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_EDUCATION_FORM)
def check_education_form(message):
    user_id = message.from_user.id
    education_form = message.text.strip()

    if user_id in user_data:
        fullname = user_data[user_id].get("fullname", "")
        birth_date = user_data[user_id].get("birth_date", "")
        hometown = user_data[user_id].get("hometown", "")

        # Удаляем состояние пользователя после проверки
        if user_id in user_states:
            user_states.pop(user_id)
        if user_id in user_data:
            user_data.pop(user_id)

        # Удаляем клавиатуру после выбора
        markup = types.ReplyKeyboardRemove()

        if verify_education_form(fullname, birth_date, hometown, education_form):
            bot.send_message(message.chat.id, "Вы прошли проверку.", reply_markup=markup)
        else:
            random_mentor = random.choice(mentors)
            bot.send_message(message.chat.id,
                             f"К сожалению, данные не совпадают с нашими записями. Если вам кажется, что произошла ошибка, пожалуйста, свяжитесь с кем-то из менторов, например с {random_mentor}",
                             reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, начните процесс заново с команды /chat")


@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\n"
                                          f"\n"
                                          f"Это автоматическое сообщение. Есть ты хочешь посмотреть список команд, введи /start")
        bot.message_handler(start)


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


