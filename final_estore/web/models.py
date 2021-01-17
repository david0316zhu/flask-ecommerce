from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from datetime import datetime
from random import randint



class Temp:
    counter = 0
    def __init__(self, ic_num, temperature, date, time, symptoms, contact):
        Temp.counter +=1
        self.__count = Temp.counter
        self.__temperature = temperature
        self.__ic_num = ic_num
        self.__date = date
        self.__time = time
        self.__symptoms = symptoms
        self.__contact = contact
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
    def get_symptoms(self):
        return self.__symptoms
    def get_contact(self):
        return self.__contact

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
        self.__title = title

    def set_info(self, info):
        self.__info = info
    
    def set_price(self, price):
        self.__price = price

class Cart:
    def __init__(self, product, quantity):
        self.__product = product
        self.__quantity = quantity

    def get_product(self):
        return self.__product
    
    def get_quantity(self):
        return self.__quantity
    
    def get_subtotal(self):
        return "{:.2f}".format(self.__quantity * (float(self.__product.get_price())))



class Detail:
    def __init__(self, name, address, date, time):
        self.__name = name
        self.__address = address
        self.__date = date
        self.__time = time

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address
    
    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

class Order:
    def __init__(self, name1, address1, date1, time1, card, number, expire, code):
        self.__order_id = "%0.12d" % randint(0,999999999999)
        self.__name1 = name1
        self.__address1 = address1
        self.__date1 = date1
        self.__time1 = time1
        self.__card = card
        self.__number = number
        self.__expire = expire
        self.__code = code

    def get_order_id(self):
        return self.__order_id

    def get_name1(self):
        return self.__name1

    def get_address1(self):
        return self.__address1
    
    def get_date1(self):
        return self.__date1

    def get_time1(self):
        return self.__time1

    def get_card(self):
        return self.__card

    def get_number(self):
        return self.__number

    def get_expire(self):
        return self.__expire
    
    def get_code(self):
        return self.__code