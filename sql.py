from psycopg2 import connect, OperationalError, Error
from os import getenv
from direnv import load


class MySQL(object):
    def __init__(self):
        try:
            load()
            DATABASE = getenv('POSTGRES_DATABASE')
            HOST = getenv('POSTGRES_HOST')
            USER = getenv('POSTGRES_USER')
            PASSWORD = getenv('POSTGRES_PASSWORD')
            self.connect = connect(database=DATABASE,
                                   user=USER,
                                   password=PASSWORD,
                                   host=HOST)
        except OperationalError as error:
            print('Can not connect', error)
            return
        try:
            self.cursor = self.connect.cursor()
        except OperationalError as error:
            print('Can not get cursor', error)
            return

    def insert_new_user(self, telegram_id, name, phone_number, sex, address):
        try:
            self.cursor.execute('''INSERT INTO public.user
                                    (telegram_id, name, phone_number, sex, address)
                                    VALUES (%s, %s, %s, %s, %s);''',
                                (telegram_id, name, phone_number, sex, address))
        except Error as error:
            print(error)
            return
        self.connect.commit()

    def check_user(self, chat_id):
        try:
            self.cursor.execute('''SELECT id
                                    FROM public.user
                                    WHERE telegram_id=(%s)''',
                                (chat_id, ))
        except Error as error:
            print(error)
            return
        data = self.cursor.fetchone()
        if data is None:
            return
        else:
            return 1

    def select_info_from_user(self, chat_id):
        try:
            self.cursor.execute('''SELECT name, phone_number, sex, address
                                    FROM public.user
                                    WHERE telegram_id=(%s)''',
                                (chat_id, ))
        except Error as error:
            print(error)
            return
        data = self.cursor.fetchone()
        return data

    def update_user_name(self, chat_id, name):
        try:
            self.cursor.execute('''UPDATE public.user
                                    SET name=(%s)
                                    WHERE telegram_id=(%s)''',
                                (name, chat_id))
        except Error as error:
            print(error)
            return
        self.connect.commit()
        return

    def update_user_sex(self, chat_id, sex):
        try:
            self.cursor.execute('''UPDATE public.user
                                    SET sex=(%s)
                                    WHERE telegram_id=(%s)''',
                                (sex, chat_id))
        except Error as error:
            print(error)
            return
        self.connect.commit()
        return

    def update_user_num(self, chat_id, num):
        try:
            self.cursor.execute('''UPDATE public.user
                                    SET phone_number=(%s)
                                    WHERE telegram_id=(%s)''',
                                (num, chat_id))
        except Error as error:
            print(error)
            return
        self.connect.commit()
        return

    def select_categories_from_category(self):
        try:
            self.cursor.execute('''SELECT name, id
                                    FROM public.category''')
        except Error as error:
            print(error)
            return
        categories = self.cursor.fetchall()
        return categories

    def select_products_from_product(self, category):
        try:
            self.cursor.execute('''SELECT id, name
                                    FROM public.product
                                    WHERE category_id=(%s)''',
                                (category, ))
        except Error as error:
            print(error)
            return
        products = self.cursor.fetchall()
        return products

    def select_product_info_from_product(self, product_id):
        try:
            self.cursor.execute('''SELECT name, price, count, type, picture_id, category_id
                                    FROM public.product
                                    WHERE id=(%s)''',
                                (product_id, ))
        except Error as error:
            print(error)
            return
        product = self.cursor.fetchone()
        return product

    def select_product_url_from_picture(self, picture_id):
        try:
            self.cursor.execute('''SELECT url
                                    FROM public.picture
                                    WHERE id=(%s)''',
                                (picture_id, ))
        except Error as error:
            print(error)
        url = self.cursor.fetchone()
        return url
