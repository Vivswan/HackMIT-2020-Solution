# -*- coding: utf-8 -*-
import requests

url = 'https://zoomlang.hackmit.academy/api/interpret'

data = {
    'username': "Vivswan_f17f03",
    'puzzlenum': "1",
    'program': "+cca",
}

while True:
    print("?")
    data['program'] = input()
    x = requests.post(url, data=data).json()

    if x.keys().__contains__('msg'):
        print(f"msg: {x['msg']}")
    if x.keys().__contains__('flag'):
        print(f"flag: {x['flag']}")
    if x.keys().__contains__('registers'):
        print(f"registers: {x['registers']}")

    data['program'] += "n"
    x = requests.post(url, data=data).json()
    if x.keys().__contains__('err'):
        print(f"err: {x['err']}")

