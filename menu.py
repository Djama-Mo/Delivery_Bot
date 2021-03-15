from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, CallbackQuery
from telebot.types import InlineKeyboardButton
import redis_cache
from message_txt import *


def menu(bot: TeleBot, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    markup = InlineKeyboardMarkup()
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _catalog = catalog_uz
        self_data = self_uz
        cart = cart_uz
        menu_but = menu_but_uz
    else:
        _catalog = catalog_ru
        self_data = self_ru
        cart = cart_ru
        menu_but = menu_but_ru
    button_catalog = InlineKeyboardButton(text=f'{_catalog} 🛍', callback_data='catalog')
    button_self = InlineKeyboardButton(text=f'{self_data} 🧾', callback_data='self')
    button_cart = InlineKeyboardButton(text=f'{cart} 🛒', callback_data='cart')
    markup.add(button_catalog, button_self).add(button_cart)
    bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)
    bot.send_message(chat_id=chat_id, text=menu_but, reply_markup=markup)


def self(bot: TeleBot, callback: CallbackQuery, sql):
    chat_id = callback.message.chat.id
    lang = redis_cache.get_language(chat_id)
    info = sql.select_info_from_user(chat_id)
    if lang == 'uz':
        name = menu_name_uz
        sex = menu_sex_uz
        num = menu_num_uz
        add = menu_address_uz
        menu_but = menu_but_uz
        change_name = change_name_uz
        change_num = change_num_uz
        change_sex = change_sex_uz
        if int(info[2]) == 1:
            sex_val = menu_sex_val_m_uz
        else:
            sex_val = menu_sex_val_f_uz
    else:
        name = menu_name_ru
        sex = menu_sex_ru
        num = menu_num_ru
        add = menu_address_ru
        menu_but = menu_but_ru
        change_name = change_name_ru
        change_num = change_num_ru
        change_sex = change_sex_ru
        if int(info[2]) == 1:
            sex_val = menu_sex_val_m_ru
        else:
            sex_val = menu_sex_val_f_ru
    self_text = f'<u>{name}</u>: <b>{info[0]}</b>\n<u>{num}</u>: <b>{info[1]}</b>\n' \
                f'<u>{sex}</u>: <b>{sex_val}</b>\n<u>{add}</u>: <b>{info[3]}</b>'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=change_name, callback_data='change_name'),
               InlineKeyboardButton(text=change_num, callback_data='change_num'),
               InlineKeyboardButton(text=change_sex, callback_data='change_sex'))
    markup.add(InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)
    bot.send_message(chat_id=chat_id, text=self_text, reply_markup=markup, parse_mode='html')


def name_changed(bot: TeleBot, message):
    chat_id = message.chat.id
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _name_changed = name_changed_uz
        menu_but = menu_but_uz
    else:
        _name_changed = name_changed_ru
        menu_but = menu_but_ru
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    bot.send_message(chat_id=chat_id, text=_name_changed, reply_markup=markup)


def num_changed(bot: TeleBot, message):
    chat_id = message.chat.id
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _num_changed = num_changed_uz
        menu_but = menu_but_uz
    else:
        _num_changed = num_changed_ru
        menu_but = menu_but_ru
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    bot.send_message(chat_id=chat_id, text=_num_changed, reply_markup=markup)


def sex_changed(bot: TeleBot, message):
    chat_id = message.chat.id
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _sex_changed = sex_changed_uz
        menu_but = menu_but_uz
    else:
        _sex_changed = sex_changed_ru
        menu_but = menu_but_ru
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    bot.send_message(chat_id=chat_id, text=_sex_changed, reply_markup=markup)
