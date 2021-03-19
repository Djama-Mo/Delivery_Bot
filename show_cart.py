from catalog_w_products import *


def cart(bot: TeleBot, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    products = redis_cache.get_product(chat_id)
    cart_text = ''
    overall_price = 0
    for key in products.keys():
        total_price = int(products[key]['count'] * products[key]['price'])
        overall_price += total_price
        cart_text += f'{key} - {total_price}\n'
    cart_text += f'____________________________\n{overall_price}'
    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(chat_id, cart_text)
