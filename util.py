import time
from datetime import date

#Capitilize string
def util_capit(a):
    if type(a) is str:res = str.capitalize(a)
    else: res = a
    return res

def util_add_word(german,
                  english,
                  article,
                  russian,
                  wrd_type,
                  tags,
                  dictionary):

    word = {"idx":len(dictionary),
            "english":english,
            "german":german,
            "russian":russian,
            "type":wrd_type,
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