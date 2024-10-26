import telebot
from telebot import types
from geopy.distance import great_circle

# апи
botTimeWeb = telebot.TeleBot('Your api key')
# корды скамеек (лучше бы базу данных)
locations = [['59.946065', '30.391502'], ['59.947314', '30.408196'], ['59.940747', '30.427765']]

# старт
@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name}</b>, привет!\nС помощью бота <b>BenchSpot</b> ты сможешь с облегчением присесть тогда, когда это так нужно."

    # клавиатура с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_route = types.KeyboardButton(text='Построить маршрут до ближайшей скамейки')
    button_instructions = types.KeyboardButton(text='Инструкция')
    button_about = types.KeyboardButton(text='О проекте')

    # добавляем кнопку маршрута на отдельной строке
    markup.add(button_route)
    markup.add(button_instructions, button_about)

    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

# чтобы не называть по имени несколько раз
def againBot(message):
    first_mess = f"С помощью бота <b>BenchSpot</b> ты сможешь с облегчением присесть тогда, когда это так нужно.\nВыбери действие."

    # клавиатура с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_route = types.KeyboardButton(text='Построить маршрут до ближайшей скамейки')
    button_instructions = types.KeyboardButton(text='Инструкция')
    button_about = types.KeyboardButton(text='О проекте')

    # добавляем кнопку маршрута на отдельной строке
    markup.add(button_route)
    markup.add(button_instructions, button_about)

    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


# обработка кнопок
@botTimeWeb.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Построить маршрут до ближайшей скамейки":
        # клавиатура с кнопкой запроса локации
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        botTimeWeb.send_message(message.chat.id, "Поделитесь своим местоположением:", reply_markup=keyboard)

    elif message.text == "О проекте":
        mess_about = "О проекте:\n\nРазработка прекращена на неопределенный срок\nС вопросами или чем-либо другим обращаться к @metmtd"
        # клавиатура с кнопкой назад
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back = types.KeyboardButton(text='Назад в меню')
        markup.add(button_back)

        botTimeWeb.send_message(message.chat.id, mess_about, reply_markup=markup)

    elif message.text == "Инструкция":
        mess_instructions = f"Инструкция по использованию приложения: \n1. Построй маршрут (поддерживаются только <b>Яндекс Карты</b>)\n2. Поделись местоположением\n3. Перейди по ссылке в <b>Яндекс Карты</b>"
        # клавиатура с кнопкой назад
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back = types.KeyboardButton(text='Назад в меню')
        markup.add(button_back)

        botTimeWeb.send_message(message.chat.id, mess_instructions, parse_mode='html', reply_markup=markup)

    elif message.text == "Назад в меню":
        againBot(message)


@botTimeWeb.message_handler(content_types=['location'])
def location(message):
    if message.location is not None:
        user_coords = (message.location.latitude, message.location.longitude)

        # находим ближайшую точку
        nearest_location = min(locations, key=lambda loc: great_circle(user_coords, (float(loc[0]), float(loc[1]))).meters)

        # формируем ссылку для маршрута
        map_url = f"https://yandex.ru/maps/?rtext={user_coords[0]},{user_coords[1]}~{nearest_location[0]},{nearest_location[1]}&rtt=mt"

        response_message = f"Ближайшая скамейка обнаружена.\nМаршрут построен, перейдите по ссылке:\n{map_url}"
        botTimeWeb.send_message(message.chat.id, response_message)

        againBot(message)

# запуск бота непрерывно
botTimeWeb.infinity_polling()
