from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from datetime import datetime
from random import randint



class Temp:
    counter = 0
    def __init__(self, ic_num, temperature, date, time):
        Temp.counter +=1
        self.__count = Temp.counter
        self.__temperature = temperature
        self.__ic_num = ic_num
        self.__date = date
        self.__time = time
    def get_count_id(self):
        return self.__count
    def get_ic_num(self):
        return self.__ic_num
    def get_temperature(self):
        return self.__temperature
    def get_date(self):
        return self.__date
    def get_time(self):
        return self.__time

class User:
    count_id = 0

    def __init__(self, email, password):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

class Product:
    
    
    def __init__(self, title, info, price):
        self.__product_id = "%0.12d" % randint(0,999999999999)
        self.__title = title
        self.__info = info
        self.__price = price
    
    def get_product_id(self):
        return self.__product_id

    def get_title(self):
        return self.__title

    def get_info(self):
        return self.__info
    
    def get_price(self):
        return self.__price

    def set_title(self, title):
        return self.__title

    def set_info(self, info):
        return self.__info
    
    def set_price(self, price):
        return self.__price