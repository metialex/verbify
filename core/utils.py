import time
from datetime import date
import configparser
import hashlib


def capitalize(a):
    """
    Capitalize string
    """
    if type(a) is str:res = str.capitalize(a)
    else: res = a
    return res

def add_word(german,
             english,
             article,
             russian,
             word_type,
             tags,
             dictionary):

    word = {"idx":len(dictionary),
            "english":english,
            "german":german,
            "russian":russian,
            "type":word_type,
            "article":article,
            "num_practiced":0,
            "num_success":0,
            "learned":False,
            "time_added":time.strftime("%H:%M:%S"),
            "date_added":date.today().strftime("%d/%m/%Y"),
            "tags":tags,
            "last_success":0}
    
    dictionary = dictionary.append(word, ignore_index=True)
    return dictionary

def check_login(input_username: str, input_password: str) -> bool:
    """
    Search in credentials database.
    Return True if pair user/pass correct.
    """
    config = configparser.ConfigParser()
    config.read("data/credentials.ini")
    try:
        password = config.get(section='credentials', option=input_username)
    except configparser.NoOptionError:
        return False
    else:
        hashed_password = hashlib.sha256(bytes(input_password, encoding='utf-8')).hexdigest()
        if hashed_password == password:
            return True
        else:
            return False

def signup(input_username: str, input_password: str) -> bool:
    """
    Search in credentials database.
    Write to .ini config and return True if username uniq.
    """
    config = configparser.ConfigParser()
    config.read("data/credentials.ini")
    try:
        config.get(section='credentials', option=input_username)
    except configparser.NoOptionError:
        hashed_password = hashlib.sha256(bytes(input_password, encoding='utf-8')).hexdigest()
        config.set('credentials', input_username, hashed_password)
        with open('../data/credentials.ini', 'w') as update_config:
            config.write(update_config)
        return True
    else:
        return False
