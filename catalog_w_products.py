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
        return
    chat_id = message.chat.id
    products = sql.select_products_from_product(category)
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        select = select_uz
        menu_but = menu_but_uz
        back = back_uz
    else:
        select = select_ru
        menu_but = menu_but_ru
        back = back_ru
    markup = InlineKeyboardMarkup()
    for _product in products:
        markup.add(InlineKeyboardButton(text=_product[1], callback_data=f'prod_{_product[0]}'))
    markup.add(InlineKeyboardButton(text=back, callback_data='catalog'),
               InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    bot.send_message(chat_id=chat_id, text=select, reply_markup=markup)


def show_product(bot: TeleBot, message, sql, product_id):
    try:
        product_id = int(product_id)
    except ValueError as error:
        print(error)
        print(product_list.__name__)
        return
    chat_id = message.chat.id
    product = sql.select_product_info_from_product(product_id)
    if product is None:
        return
    name = product[0]
    price = product[1]
    count = product[2]
    _type = product[3]
    picture_id = product[4]
    category_id = product[5]
    product_url = None
    if picture_id is not None:
        product_url = sql.select_product_url_from_picture(picture_id)
    lang = redis_cache.get_language(chat_id)
    if lang == 'uz':
        menu_but = menu_but_uz
        back = back_uz
        product_name = product_name_uz
        product_price = product_price_uz
        product_count = product_count_uz
        product_add = product_add_uz
        product_delete = product_delete_uz
    else:
        menu_but = menu_but_ru
        back = back_ru
        product_name = product_name_ru
        product_price = product_price_ru
        product_count = product_count_ru
        product_add = product_add_ru
        product_delete = product_delete_ru
    caption = f'<u>{product_name}</u>: <b>{name}</b>\n' \
              f'<u>{product_price} {_type}</u>: <b>{price}</b>\n' \
              f'<u>{product_count}</u>: <b>{count} {_type}</b>'
    if _type == "кг":
        tmp_count = 0.5
    else:
        tmp_count = 1
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f'{product_add} {tmp_count}{_type}', callback_data=f'add_{product_id}'),
               InlineKeyboardButton(text=f'{product_delete} {tmp_count}{_type}', callback_data=f'del_{product_id}'))
    markup.add(InlineKeyboardButton(text=back, callback_data=f'cat_{category_id}'),
               InlineKeyboardButton(text=menu_but, callback_data='menu'))
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    if product_url is not None:
        bot.send_photo(chat_id=chat_id, photo=product_url[0], caption=caption, parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(chat_id=chat_id, text=caption, parse_mode='html', reply_markup=markup)
