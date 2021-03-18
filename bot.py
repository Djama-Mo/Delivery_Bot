from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import CallbackQuery
from telebot.types import Message
from direnv import load
from os import getenv
import redis_cache
import re
from sql import MySQL
from patterns import *
from message_txt import *
from get_location import send_venue
from intro_functions import req_fio, req_sex, req_num, req_geo
from catalog_w_products import (menu, self, name_changed, num_changed, sex_changed, catalog, product_list, show_product)


load()
TOKEN = getenv('TOKEN')
bot = TeleBot(TOKEN)


def main():
    bot.polling(none_stop=True)


@bot.callback_query_handler(func=lambda callback: True)
def query_messages(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    data = callback.data
    if data == 'ru' or data == 'uz':  # Language selected
        redis_cache.set_language(chat_id, data)
        if sql.check_user(chat_id) == 1:
            menu(bot, callback)
        else:
            req_fio(bot, callback)
    elif data == 'menu':
        menu(bot, callback)
    elif data == 'catalog':
        catalog(bot, callback.message, sql)
    elif 'cat_' in data:  # Selected category
        product_list(bot, callback.message, sql, data[4:])
    elif 'prod_' in data:  # Selected product
        show_product(bot, callback.message, sql, data[5:])
    elif 'add_' in data:  # Add product
        product_id = int(data[4:])
        if redis_cache.set_product(chat_id, product_id, sql) is True:
            bot.answer_callback_query(callback.id, text='OK', show_alert=True)
    elif 'del_' in data:  # Delete product
        product_id = int(data[4:])
        if redis_cache.del_product(chat_id, product_id, sql) is True:
            bot.answer_callback_query(callback.id, text='OK', show_alert=True)
    elif data == 'self':  # Profile
        self(bot, callback, sql)
    elif 'place_' in data:  # Place selected
        menu(bot, callback)
    elif 'change' in data:  # Change user's data
        redis_cache.set_change_flag(chat_id)
        if 'name' in data:
            req_fio(bot, callback)
        elif 'num' in data:
            bot.delete_message(chat_id, callback.message.message_id)
            req_num(bot, chat_id)
        else:  # sex
            bot.delete_message(chat_id, callback.message.message_id)
            req_sex(bot, callback.message)
    elif 'sex' in data:  # Sex selected
        sex = data[-1]
        if sex == 'm':
            sex = 1
        else:
            sex = 0
        if redis_cache.get_change_flag(chat_id) is None:
            req_geo(bot, chat_id)
            redis_cache.set_user_sex(chat_id, sex)
        else:
            sql.update_user_sex(chat_id, sex)
            sex_changed(bot, callback.message)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    markup = InlineKeyboardMarkup()
    chat_id = message.chat.id
    if message.message_id > 1:
        try:
            bot.delete_message(chat_id, message.message_id - 1)
        except ApiTelegramException:
            pass
    bot.delete_message(chat_id, message.message_id)
    button_ru = InlineKeyboardButton(rus, callback_data='ru')
    button_uz = InlineKeyboardButton(uzb, callback_data='uz')
    markup.add(button_uz).add(button_ru)
    bot.send_message(chat_id=chat_id, text=hello, reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['contact'])
def contact(message: Message):
    if message.contact is not None:
        if redis_cache.get_change_flag(message.chat.id) is None:
            req_sex(bot, message)
            redis_cache.set_user_number(message.chat.id, message.contact.phone_number)
        else:
            sql.update_user_num(message.chat.id, message.contact.phone_number)
            bot.delete_message(message.chat.id, message.message_id - 1)
            num_changed(bot, message)


sql = MySQL()


@bot.message_handler(func=lambda message: True, content_types=['location'])
def location(message: Message):
    send_venue(message, bot)
    user_info = redis_cache.get_user_full_info(message.chat.id)
    if user_info is not None:
        sql.insert_new_user(int(message.chat.id), str(user_info[0]),
                            str(user_info[1]), int(user_info[2]), str(user_info[3]))


@bot.message_handler(func=lambda message: True)
def buttons_tree(message: Message):
    chat_id = message.chat.id
    if re.fullmatch(pattern=fio_pattern, string=message.text):
        if redis_cache.get_change_flag(chat_id) is None:
            req_num(bot, chat_id=chat_id)
            redis_cache.set_user_name(chat_id, message.text)
        else:
            sql.update_user_name(chat_id, message.text)
            bot.delete_message(message.chat.id, message.message_id - 1)
            name_changed(bot, message)
    elif re.fullmatch(pattern=phone_number_pattern, string=message.text):
        if redis_cache.get_change_flag(chat_id) is None:
            req_sex(bot, message)
            redis_cache.set_user_number(chat_id, message.text)
        else:
            sql.update_user_num(chat_id, message.text)
            num_changed(bot, message)


if __name__ == '__main__':
    main()
