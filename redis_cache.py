# import logging
from redis import Redis, RedisError


rediska = Redis()

def write_language(chat_id, language):
    try:
        rediska.set(name=f'{chat_id}_lang', value=language, ex=21600)
    except RedisError as error:
        print(error)
        print(write_language.__name__)
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


def write_user_name(chat_id, name):
    try:
        rediska.set(f'{chat_id}_name', name, ex=1800)
    except RedisError as error:
        print(error)
        print(write_user_name.__name__)
        return


def write_user_number(chat_id, number):
    try:
        rediska.set(f'{chat_id}_number', number, ex=1800)
    except RedisError as error:
        print(error)
        print(write_user_number.__name__)
        return


def write_user_sex(chat_id, sex):
    try:
        rediska.set(f'{chat_id}_sex', sex, ex=1800)
    except RedisError as error:
        print(error)
        print(write_user_sex.__name__)
        return


def write_user_address(chat_id, address):
    try:
        rediska.set(f'{chat_id}_address', address, ex=1800)
    except RedisError as error:
        print(error)
        print(write_user_address.__name__)
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


def write_change_flag(chat_id):
    try:
        rediska.set(f'{chat_id}_change', 1, ex=1800)
    except RedisError as error:
        print(error)
        print(write_user_address.__name__)
        return


def get_change_flag(chat_id):
    try:
        flag = rediska.get(f'{chat_id}_change')
    except RedisError as error:
        print(error)
        print(write_user_address.__name__)
        return
    if flag is None:
        return
    else:
        rediska.delete(f'{chat_id}_change')
        return flag.decode()
