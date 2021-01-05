from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from datetime import datetime




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
