from telebot import TeleBot
from telebot.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup,\
                            ReplyKeyboardMarkup, KeyboardButton
import redis_cache
from message_txt import *


def req_fio(bot, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        fio = fio_uz
    else:
        fio = fio_ru
    bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)
    bot.send_message(chat_id=chat_id, text=fio)


def req_num(bot: TeleBot, chat_id):
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _req_num = req_num_uz
        req_num_but = req_num_but_uz
    else:
        _req_num = req_num_ru
        req_num_but = req_num_but_ru
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_contact = KeyboardButton(text=req_num_but, request_contact=True)
    markup.add(button_contact)
    bot.send_message(chat_id=chat_id, text=_req_num, reply_markup=markup)


def req_sex(bot, message: Message):
    markup = InlineKeyboardMarkup()
    chat_id = message.chat.id
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        sex = sex_uz
    else:
        sex = sex_ru
    button_1 = InlineKeyboardButton(text=sex_but_m, callback_data='sex_m')
    button_2 = InlineKeyboardButton(text=sex_but_w, callback_data='sex_w')
    markup.add(button_1, button_2)
    bot.send_message(chat_id=chat_id, text=sex, reply_markup=markup)


def req_geo(bot, chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _req_geo = req_geo_uz
        req_geo_but = req_geo_but_uz
    else:
        _req_geo = req_geo_ru
        req_geo_but = req_geo_but_ru
    button_contact = KeyboardButton(text=req_geo_but, request_location=True)
    markup.add(button_contact)
    bot.send_message(chat_id=chat_id, text=_req_geo, reply_markup=markup)
