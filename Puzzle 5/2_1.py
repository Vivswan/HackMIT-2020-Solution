# -*- coding: utf-8 -*-
import itertools

from a import run

OFFW = []
WRONG = []
SUPERWRONG = []

# arr_char = ['y', 'f', 's', '+']
arr_char = ['y', '+', 's', 'f', 'b', 'a', 'c']
all_char = ''.join(arr_char)
all_char_reg_ex = all_char.replace('-', '\-')


def generate_strings(length=4):
    for item in itertools.product(all_char, repeat=length):
        i = "".join(item)
        if i.__contains__('c') and i[0] != 'y' and i[0] != 'f':
            yield i


def main():
    for i in generate_strings():
        try:
            run(i, False, False, False)
        except:
            # print(f"err problem: {i}")
            pass

    print(WRONG)
    print(SUPERWRONG)
    print(OFFW)


if __name__ == "__main__":
    main()
