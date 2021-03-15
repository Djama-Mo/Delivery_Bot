from menu import *


def catalog(bot, message, sql):
    chat_id = message.chat.id
    categories = sql.select_categories_from_category()
    if categories is None:
        return
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        _categories = category_uz
        menu_but = menu_but_uz
    else:
        _categories = category_ru
        menu_but = menu_but_ru
    markup = InlineKeyboardMarkup()
    for category in categories:
        markup.add(InlineKeyboardButton(text=category[0], callback_data=f'cat_{category[1]}'))
    markup.add(InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    bot.send_message(chat_id=chat_id, text=_categories, reply_markup=markup)


def product_list(bot, message, sql, category):
    try:
        category = int(category)
    except ValueError as error:
        print(error)
        print(product_list.__name__)
    chat_id = message.chat.id
    products = sql.select_products_from_product(category)
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        select = select_uz
        menu_but = menu_but_uz
    else:
        select = select_ru
        menu_but = menu_but_ru
    markup = InlineKeyboardMarkup()
    for _product in products:
        markup.add(InlineKeyboardButton(text=_product[1], callback_data=f'prod_{_product[0]}'))
    markup.add(InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    bot.send_message(chat_id=chat_id, text=select, reply_markup=markup)


def show_product(bot, message, sql, product):
    pass
