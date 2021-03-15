from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from places import *
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from telebot import TeleBot
import redis_cache
from message_txt import choose_place_uz, choose_place_ru


def location(message: Message):
    lat = message.location.latitude
    long = message.location.longitude
    geolocator = Nominatim(user_agent="MarDel_Bot")
    loc = geolocator.reverse(f'{lat}, {long}').address
    redis_cache.write_user_address(message.chat.id, loc)
    nearly_places = []
    index = 0
    for place in places:
        distance = geodesic((place['latitude'], place['longitude']), (lat, long)).kilometers
        if distance <= 2:
            nearly_places.append(index)
        index += 1
    return nearly_places


def text(count):
    message_text = f'Рядом с Вами {count} '
    if count == 1:
        message_text += 'отель'
    elif count == 2 or count == 3 or count == 4:
        message_text += 'отеля'
    else:
        message_text += 'отелей'
    return message_text


def send_venue(message: Message, bot: TeleBot):
    nearly_places = location(message)
    count = len(nearly_places)
    buttons = []
    lang = redis_cache.get_language(message.chat.id)
    if lang == 'uz':
        txt = f'Sizga yaqin {count} mehmonxona'
    else:
        txt = text(count)
    bot.send_message(chat_id=message.chat.id, text=txt)
    for place in nearly_places:
        buttons.append(InlineKeyboardButton(text=places[place]['title'], callback_data=f'place_{place}'))
        bot.send_venue(chat_id=message.chat.id,
                       latitude=places[place]['latitude'],
                       longitude=places[place]['longitude'],
                       title=places[place]['title'],
                       address=places[place]['address'])
    markup = InlineKeyboardMarkup()
    for button in buttons:
        markup.add(button)
    if len(buttons) > 0:
        if lang == 'uz':
            txt = choose_place_uz
        else:
            txt = choose_place_ru
        bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=markup)
