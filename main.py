import random
from bot_init import bot
from telebot import types # type: ignore

from csv_database import check_full_name, verify_birth_date, verify_hometown, verify_education_form

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
                                      f"Я - бот менторской программы ФМО, пытаться со мной говорить бесполезно, однако я всё ещё могу тебе помочь! Вот команды, с которыми я работаю:\n"
                                      f"\n"
                                      f"<b>/mentor</b> - я дам тебе ссылки на представителей менторской программы, они смогут рассказать тебе побольше про СПбГУ и наш факультет\n"
                                      f"\n"
                                      f"<b>/links</b> - я дам тебе ссылки на все самые важные ресурсы для любого международника\n"
                                      f"\n"
                                      f"<b>/chat</b> - я дам тебе ссылку на чат твоего потока. \n"
                                      f"<b>Важно! Беседа появится не раньше 15 августа, потому что мы ждём, когда появятся списки всех поступивших</b>\n"
                                      f"\n"
                                      f"<b>/pamatka</b> - я дам тебе ссылку на священный грааль - памятку первокурсника. В ней ты найдёшь ответы на все вопросы, которые могут у тебя возникнуть\n"
                                      f"\n"
                                      f"<b>/subscribe</b> - подписка на рассылку новостей от Менторской Программы",
                     parse_mode='html')


@bot.message_handler(commands=['pamatka'])
def pamatka_command(message):
    pamatka = types.InlineKeyboardMarkup()
    pamatka.add(types.InlineKeyboardButton('Почитать памятку', url='https://disk.yandex.ru/d/XElmsMv8yYqVZg'))
    bot.send_message(message.chat.id,
                     f'Наши заботливые менторы подготовили для тебе незаменимую штуку🚸, а в чате со мной ты её никогда не потеряешь🗺️',
                     reply_markup=pamatka)


@bot.message_handler(commands=['mentor'])
def mentor_command(message):
    # EN: Create an inline keyboard with a button to view the guide (pamjatka)
    # RU: Создаём inline-клавиатуру с кнопкой для просмотра памятки
    mentor = types.InlineKeyboardMarkup(row_width=1)  # EN: row_width=1 for mobile-friendly, RU: row_width=1 для мобильной дружелюбности
    mentor.add(
        types.InlineKeyboardButton(
            text='Смотреть памятку', 
            url='https://disk.yandex.ru/d/XElmsMv8yYqVZg'
        )
    )
    # EN: Prepare the full mentor message, keeping it mobile-friendly and in Russian
    # RU: Готовим полное сообщение о менторах, делаем его удобным для мобильных и на русском
    mentor_message = (
        "По всем вопросам ты можешь написать любому из наших менторов ✨!\n"
        "\n"
        "\n"
        "Вот наши 'узко направленные' специалисты по основным направлениям:\n"
        "\n"
        "✈️Иностранец? Тебе к @Polly_uu \n"
        "\n"
        "🏘️Нужна помощь с общежитием? @nanysua \n"
        "\n"
        "📩Административные вопросы (учебка, стипендии и т.п): @PolLinaaa_Ma \n"
        "\n"
        "📚Все-все учебные вопросы: @milenazavr \n"
        "\n"
        "🪩А если хочешь знать чем заняться на факультете помимо учебы: @correttoo \n"
        "\n"
        "📝По вопросам поступления пиши @mitrunya и почта приёмной комиссии ir@priem.spbu.ru \n"
        "\n"
        "\n"
        "Прежде чем писать ментору, проверь, нет ли ответа на твой вопрос в [памятке первокурсника](https://disk.yandex.ru/d/XElmsMv8yYqVZg) \n"
        "\n"
        "<b>Пожалуйста, помни, что ментор может не всегда быть на связи, особенно, если ты пишешь посреди ночи.</b>\n"
    )
    # EN: Send the message with the inline keyboard
    # RU: Отправляем сообщение с клавиатурой
    bot.send_message(
        message.chat.id,
        mentor_message,
        parse_mode='html',
        reply_markup=mentor
    )


# EN: Handler for the '/links' command. Sends a list of useful program resources.
# RU: Обработчик команды '/links'. Отправляет список полезных ресурсов программы.

@bot.message_handler(commands=['links'])
def links_command(message):
    # EN: Prepare the message with all links, using HTML formatting for bold sections.
    # EN: Prepare the message with all links, using HTML formatting for bold sections.
    # RU: Готовим сообщение со всеми ссылками, используя HTML для выделения жирным.
    links_message = (
        "🖇️Новости, мемы,студсовет: это все тут\n"
        "\n"
        "Ресурсы менторской программы:\n"  # EN: Mentor program resources / RU: Ресурсы менторской программы
        "ТГК: https://t.me/mentorkafmo\n"  # EN: Telegram channel / RU: Телеграм-канал
        "ВК: https://vk.com/mentorka_fmo\n"  # EN: VK group / RU: Группа ВК
        "\n"
        "<b>Студенческий Совет</b>:\n"  # EN: Student Council (bold) / RU: Студенческий Совет (жирным)
    "ФМО https://vk.com/sirspbu\n"
    "СПбГУ https://vk.com/ssspbu\n"
    "\n"
    "<b>Прочие каналы</b>:\n"
    "Студенческое Научное Общество - https://vk.com/snofmo\n"
    "Смольный Знает (ВК) - https://vk.com/smolnyknows\n"
    "Смольный Знает (ТГ) - https://t.me/smolnyknows\n"
    "Клуб Молодёжной Дипломатии - https://t.me/dipclub_spbu\n"
    "Смольный Флекс - https://vk.com/smolnyflex"
    )
  

    # EN: The following line sends the full list of useful links to the user, using HTML formatting for better readability on mobile devices.
    # RU: Следующая строка отправляет пользователю полный список полезных ссылок, используя HTML-разметку для лучшей читаемости на мобильных устройствах.
    bot.send_message(
        message.chat.id,         # EN: The chat ID to send the message to / RU: ID чата, куда отправляется сообщение
        links_message,           # EN: The message with all links / RU: Сообщение со всеми ссылками
        parse_mode='html'        # EN: Enable HTML formatting for the message / RU: Включаем HTML-разметку для сообщения
    )

@bot.message_handler(commands=['chat'])
def chat_command(message):
    user_id = message.from_user.id
    user_states[user_id] = AWAITING_NAME
    user_data[user_id] = {}
    # random_mentor удалён, убираем из сообщения
    bot.send_message(message.chat.id,
                     f"Чтобы попасть в чат, тебе нужно пройти небольшую проверку. Это сделано, чтобы в чате могли оказаться только настоящие первокурсники. Пожалуйста, напиши своё ФИО как в паспорте. \n"
                     f"\n"
                     f"<b>Пример: Иванов Иван Иванович</b>\n"
                     f"\n"
                     f"Если ты иностранный студент, пожалуйста, обратись к одному из менторов.", parse_mode='html')


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_NAME)
def check_fullname(message):
    user_id = message.from_user.id
    fullname = message.text.strip()

    is_valid, student_data = check_full_name(fullname)

    if is_valid:
        user_data[user_id]["fullname"] = fullname
        user_states[user_id] = AWAITING_BIRTH_DATE
        bot.send_message(message.chat.id, "Напиши свою дату рождения в формате ДД.ММ.ГГГГ\n"
                                          "\n"
                                          "<b>Пример: 01.01.2000</b>", parse_mode='html')
    else:
        if user_id in user_states:
            user_states.pop(user_id)
        if user_id in user_data:
            user_data.pop(user_id)
        # random_mentor удалён, убираем из сообщения
        bot.send_message(message.chat.id,
                         f"К сожалению, тебя нет в списках на поступление. Если тебе кажется, что произошла ошибка, пожалуйста, свяжись с кем-то из менторов.")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_BIRTH_DATE)
def check_birth_date(message):
    user_id = message.from_user.id
    birth_date = message.text.strip()

    if user_id in user_data:
        fullname = user_data[user_id].get("fullname", "")

        if verify_birth_date(fullname, birth_date):
            user_data[user_id]["birth_date"] = birth_date
            user_states[user_id] = AWAITING_HOMETOWN
            bot.send_message(message.chat.id, "Пожалуйста, введи свой город рождения \n"
                                              "\n"
                                              "<b>пример: Санкт-Петербург</b>", parse_mode='html')
        else:
            if user_id in user_states:
                user_states.pop(user_id)
            if user_id in user_data:
                user_data.pop(user_id)
            # random_mentor удалён, убираем из сообщения
            bot.send_message(message.chat.id,
                             f"К сожалению, данные не совпадают с нашими записями. Если тебе кажется, что произошла ошибка, пожалуйста, свяжись с кем-то из менторов.")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, начни процесс заново с команды /chat")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == AWAITING_HOMETOWN)
def check_hometown(message):
    user_id = message.from_user.id
    hometown = message.text.strip()

    if user_id in user_data:
        fullname = user_data[user_id].get("fullname", "")
        birth_date = user_data[user_id].get("birth_date", "")

        if verify_hometown(fullname, birth_date, hometown):
            user_data[user_id]["hometown"] = hometown
            user_states[user_id] = AWAITING_EDUCATION_FORM

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton('Бюджетная')
            btn2 = types.KeyboardButton('Договорная')
            markup.add(btn1, btn2)

            bot.send_message(message.chat.id, "Пожалуйста, укажи форму вашего обучения:", reply_markup=markup)
        else:
            if user_id in user_states:
                user_states.pop(user_id)
            if user_id in user_data:
                user_data.pop(user_id)
            # random_mentor удалён, убираем из сообщения
            bot.send_message(message.chat.id,
                             f"К сожалению, данные не совпадают с нашими записями. Если тебе кажется, что произошла ошибка, пожалуйста, свяжись с кем-то из менторов.")
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
            bot.send_message(message.chat.id, "Успешное прохождение опроса, тут в конечной версии будет ссылка на чат.", reply_markup=markup)
        else:
            # random_mentor удалён, убираем из сообщения
            bot.send_message(message.chat.id,
                             f"К сожалению, данные не совпадают с нашими записями. Если вам кажется, что произошла ошибка, пожалуйста, свяжитесь с кем-то из менторов.",
                             reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, начните процесс заново с команды /chat")