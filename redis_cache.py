# import logging
from redis import Redis, RedisError
from json import loads


rediska = Redis()

def set_language(chat_id, language):
    try:
        rediska.set(name=f'{chat_id}_lang', value=language, ex=21600)
    except RedisError as error:
        print(error)
        print(set_language.__name__)
        return


def get_language(chat_id):
    try:
        language = rediska.get(f'{chat_id}_lang').decode()
    except RedisError as error:
        print(error)
        print(get_language.__name__)
        return 'ru'
    except AttributeError as error:
        print(error)
        print(get_language.__name__)
        return 'ru'
    if language is None:
        return 'ru'
    return language


def set_user_name(chat_id, name):
    try:
        rediska.set(f'{chat_id}_name', name, ex=1800)
    except RedisError as error:
        print(error)
        print(set_user_name.__name__)
        return


def set_user_number(chat_id, number):
    try:
        rediska.set(f'{chat_id}_number', number, ex=1800)
    except RedisError as error:
        print(error)
        print(set_user_number.__name__)
        return


def set_user_sex(chat_id, sex):
    try:
        rediska.set(f'{chat_id}_sex', sex, ex=1800)
    except RedisError as error:
        print(error)
        print(set_user_sex.__name__)
        return


def set_user_address(chat_id, address):
    try:
        rediska.set(f'{chat_id}_address', address, ex=1800)
    except RedisError as error:
        print(error)
        print(set_user_address.__name__)
        return


def get_user_full_info(chat_id):
    info = []
    try:
        info.append(rediska.get(f'{chat_id}_name').decode('utf-8'))
        rediska.delete(f'{chat_id}_name')
        info.append(rediska.get(f'{chat_id}_number').decode('utf-8'))
        rediska.delete(f'{chat_id}_number')
        info.append(rediska.get(f'{chat_id}_sex').decode('utf-8'))
        rediska.delete(f'{chat_id}_sex')
        info.append(rediska.get(f'{chat_id}_address').decode('utf-8'))
        rediska.delete(f'{chat_id}_address')
    except RedisError as error:
        print(error)
        print(get_user_full_info.__name__)
        return
    except AttributeError as error:
        print(error)
        print(get_user_full_info.__name__)
        return
    return info


def set_change_flag(chat_id):
    try:
        rediska.set(f'{chat_id}_change', 1, ex=1800)
    except RedisError as error:
        print(error)
        print(set_user_address.__name__)
        return


def get_change_flag(chat_id):
    try:
        flag = rediska.get(f'{chat_id}_change')
    except RedisError as error:
        print(error)
        print(set_user_address.__name__)
        return
    if flag is None:
        return
    else:
        rediska.delete(f'{chat_id}_change')
        return flag.decode()


def get_product(chat_id) -> dict:
    try:
        product = rediska.get(f'{chat_id}_product')
    except RedisError as error:
        print(error)
        print(get_product.__name__)
        return dict()
    if product is None:
        return dict()
    else:
        return loads(product.decode('utf-8'))


def set_product(chat_id, product_id, sql):
    _product = sql.select_product_info_from_product(product_id)
    if _product is None:
        return False
    name = _product[0]
    price = _product[1]
    left = _product[2]
    _type = _product[3]
    if _type == 'кг':
        count = 0.5
    else:
        count = 1
    try:
        price = int(price)
        left = float(left)
    except ValueError as error:
        print(error)
        print(set_product.__name__)
        return False
    key_str = '{"%s": ' \
              '{"id": %s,' \
              '"count": %s,' \
              '"price": %s' \
              '}' \
              '}'
    product = get_product(chat_id)
    old_count = 0
    try:
        old_count = product[name]['count']
    except KeyError:
        pass
    new_count = old_count + count
    if new_count > left:
        return f'{name} - {new_count}{_type}\nMAX'
    key = key_str % (name, product_id, new_count, price)
    product.update(loads(key))
    rediska.set(f'{chat_id}_product', str(product).replace("'", '"'), ex=86400)
    return f'{name} - {new_count}{_type}'


def del_product(chat_id, product_id, sql):
    _product = sql.select_product_info_from_product(product_id)
    if _product is None:
        return False
    name = _product[0]
    _type = _product[3]
    if _type == 'кг':
        count = 0.5
    else:
        count = 1
    product = get_product(chat_id)
    new_count = 0
    try:
        if product[name]['count'] == count:
            del product[name]
        elif product[name]['count'] > count:
            product[name]['count'] -= count
            new_count = product[name]['count']
        rediska.set(f'{chat_id}_product', str(product).replace("'", '"'), ex=86400)
    except KeyError as error:
        print(error)
        print(set_product.__name__)
        return False
    return f'{name} - {new_count}{_type}'
