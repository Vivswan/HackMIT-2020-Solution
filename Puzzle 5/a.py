# -*- coding: utf-8 -*-
import itertools
import math
import random

import requests
import re
import json

VERBOSE = True
SEARCH = False
STOPSEARCH = False
OFFW = []
WRONG = []
SUPERWRONG = []

arr_char = ['y', 'f', 's', '+', 'c', 'b', 'a']
# arr_char = ['y', '+', '-', 'b', 'a']
all_char = ''.join(arr_char)
all_char_reg_ex = all_char.replace('-', '\-')

# pattern = re.compile("^[\+\-sc]+[" + all_char_reg_ex + "]*(b[" + all_char_reg_ex + "]+a)*[" + all_char_reg_ex + "]*$")
# print(pattern.pattern)


def generate_strings(length=5):
    global all_char
    for item in itertools.product(all_char, repeat=length):
        i = "".join(item)
        # if re.search(pattern, i) is not None:
        yield i


# noinspection DuplicatedCode
def online(prog):
    url = 'https://zoomlang.hackmit.academy/api/interpret'
    data = {
        'username': "Vivswan_f17f03",
        'puzzlenum': "2",
        'program': prog,
    }
    r = {
        'err': None,
        'msg': None,
        'flag': None
    }
    x = requests.post(url, data=data).json()
    data['program'] += "n"
    if not SEARCH:
        y = requests.post(url, data=data).json()
        if y.keys().__contains__('err'):
            r['err'] = y['err']
            xx = r['err'].split('\n')
            r['pc'] = int(xx[0].split('=')[1].strip())
            r['pc_dir'] = int(xx[1].split('=')[1].strip())
            r['step'] = int(xx[2].split('=')[1].strip())
            r['unused_breaks'] = json.loads(xx[3].split('=')[1].strip())
            r['used_breaks'] = json.loads(xx[4].split('=')[1].strip())
            r['cur_reg'] = int(xx[5].split('=')[1].strip())
            if xx[6].split('=')[1].strip() == 'none':
                r['prev_reg'] = None
            else:
                r['prev_reg'] = int(xx[6].split('=')[1].strip())
            r['reg_dir'] = int(xx[7].split('=')[1].strip())
            r['steps_per_reg'] = json.loads(xx[8].split('=')[1].strip())
            r['cur_reg_steps'] = int(xx[9].split('=')[1].strip())

    if x.keys().__contains__('registers'):
        r['registers'] = x['registers']
    if x.keys().__contains__('msg'):
        r['msg'] = x['msg']
    if x.keys().__contains__('flag'):
        r['flag'] = x['flag']

    return r


def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


def get_valid_program(seed, changes):
    global all_char
    while True:
        try:
            p = seed
            for i in range(0, changes):
                p = replacer(p, all_char[random.randint(0, len(all_char))], random.randint(0, len(seed)))
            if seed == p:
                continue
            x = run(p)
            return (p, x)
            break
        except:
            pass


def main():
    global VERBOSE, SEARCH, STOPSEARCH

    # VERBOSE = False
    # for i in generate_strings():
    #     try:
    #         run(i)
    #     except:
    #         pass
    #     if SEARCH and STOPSEARCH:
    #         break

    # VERBOSE = False
    # run('c+')
    # run('c++')
    # run('c+++')
    # run('s++')
    # run('s++')
    # run('+s+')
    # run('+sy+')
    # run('sfs+y')
    VERBOSE = True
    run('+++y')
    run('+ssc+++')
    run('+sc+')
    run('+cs+')
    run('++sss++++')
    # # run('sc+')

    # VERBOSE = False
    # SEARCH = True
    # seed = ('+' * 34) + 'ya'
    # r = run(seed)
    # # arr50 = []
    # arr50 = []
    #
    # min = ("", r * 100)
    #
    # for i in range(0, 50):
    #     x = None
    #     y = r * 5
    #     while not y < r * 1.5:
    #         x, y = get_valid_program(seed, random.randint(1, 15))
    #     arr50.append((x, y))
    #
    # while True:
    #     arr5000_p = []
    #     arr5000_y = []
    #     arr5000 = []
    #     for i in range(0, 5000):
    #         j = math.floor(i / 100)
    #         x = arr50[j][0]
    #         while True:
    #             x, y = get_valid_program(x, random.randint(1, 15))
    #             if not arr5000_p.__contains__(x) and not arr5000.__contains__(x):
    #                 break
    #         arr5000_p.append(x)
    #         arr5000_y.append(y)
    #         arr5000.append((x, y))
    #
    #     arr50 = sorted(arr5000, key=lambda student: student[1])[0:50]
    #
    #     if min[1] > arr50[0][1]:
    #         min = arr50[0]
    #
    #     print(min, arr50[0])
    #
    #     if arr50[0][1] == 0:
    #         break


def run(program, VERBOSE=VERBOSE, SEARCH=SEARCH, STOPSEARCH=STOPSEARCH):
    if VERBOSE:
        print()
        print(program)

    org = None

    registers = [0, 0, 0]

    pc = 0
    pc_dir = 1
    step = 0
    unused_breaks = []
    used_breaks = []
    cur_reg = 0
    prev_reg = None
    reg_dir = 1
    steps_per_reg = [1, 1, 1]
    cur_reg_steps = 0

    # app_cur_reg = 0
    # prev_app_cur_reg = 0

    i = 0
    while i < len(program):
        if VERBOSE and not SEARCH:
            # print(f"{step} : {cur_reg_steps} : {app_cur_reg} : {prev_reg} : {cur_reg} : {i} : {program[i]} : {steps_per_reg} : {used_breaks} : {unused_breaks} -- {registers}")
            print(f"{step} : {cur_reg_steps} : {prev_reg} : {cur_reg} : {i} : {program[i]} : {steps_per_reg} : {used_breaks} : {unused_breaks} -- {registers}")

        if program[i] == "y":
            registers[cur_reg] += registers[prev_reg]

        if program[i] == "s":
            steps_per_reg[cur_reg] += 1
            # app_cur_reg -= reg_dir

        if program[i] == "f":
            if steps_per_reg[cur_reg] <= 1:
                raise ValueError()
            steps_per_reg[cur_reg] -= 1
            # t = 0
            # for j in range(0, cur_reg + 1):
            #     t += steps_per_reg[j]
            # app_cur_reg = t - reg_dir

        if program[i] == "+":
            registers[cur_reg] += 1
        if program[i] == "-":
            registers[cur_reg] -= 1

        if program[i] == "c":
            reg_dir *= -1

        if program[i] == "b" and (unused_breaks.__contains__(i) or used_breaks.__contains__(i)):
            i += 1
            continue
        if program[i] == "b" and not unused_breaks.__contains__(i) and not used_breaks.__contains__(i):
            unused_breaks.append(i)
        if program[i] == "a" and len(unused_breaks) > 0:
            i = unused_breaks.pop()
            used_breaks.append(i)

        # n_app_cur_reg, n_cur_reg = get_reg(app_cur_reg, reg_dir, steps_per_reg)

        # if n_app_cur_reg != app_cur_reg:
        #     prev_app_cur_reg = app_cur_reg
        #     app_cur_reg = n_app_cur_reg
        #
        # if n_cur_reg != cur_reg:
        #     prev_reg = cur_reg
        #     cur_reg = n_cur_reg
        #     cur_reg_steps = 0
        # else:
        cur_reg_steps += 1
        if cur_reg_steps >= steps_per_reg[cur_reg]:
            prev_reg = cur_reg
            cur_reg += reg_dir
            cur_reg %= len(registers)
            cur_reg_steps = 0

        i += 1
        step += 1

    if VERBOSE and not SEARCH:
        # print(f"{step} : {cur_reg_steps} : {app_cur_reg} : {prev_reg} : {cur_reg} : {i} :   : {steps_per_reg} : {used_breaks} : {unused_breaks} -- {registers}")
        print(f"{step} : {cur_reg_steps} : {prev_reg} : {cur_reg} : {i} :   : {steps_per_reg} : {used_breaks} : {unused_breaks} -- {registers}")

    pc = i
    used_breaks = sorted(used_breaks)

    if step > 200:
        raise ValueError()

    if not SEARCH:
        try:
            org = online(program)
        except:
            OFFW.append(program)
            print(f"offline problem: {program}")
            return

        print_result(program, VERBOSE, cur_reg, cur_reg_steps, org, pc, pc_dir, prev_reg, reg_dir, registers, step, steps_per_reg, unused_breaks, used_breaks)
    else:
        if not VERBOSE:
            value = 63245986
            if registers.__contains__(value):
                result = online(program)
                print(f"Success (2): {program} --> {registers}, {result['flag']}, {result['msg']},")
                STOPSEARCH = True
            return pow(max(registers) - value, 2)
    return None


def print_result(program, VERBOSE, cur_reg, cur_reg_steps, org, pc, pc_dir, prev_reg, reg_dir, registers, step, steps_per_reg, unused_breaks, used_breaks):
    x = True
    x = x and (org['registers'] == registers)
    x = x and (org['pc'] == pc)
    x = x and (org['pc_dir'] == pc_dir)
    x = x and (org['step'] == step)
    x = x and (org['unused_breaks'] == unused_breaks)
    x = x and (org['used_breaks'] == used_breaks)
    x = x and (org['reg_dir'] == reg_dir)
    x = x and (org['steps_per_reg'] == steps_per_reg)
    x = x and (org['cur_reg'] == cur_reg)
    x = x and (org['prev_reg'] == prev_reg)
    if program[-1] == 's' and program[-1] == 'f':
        x = x and (org['cur_reg_steps'] == cur_reg_steps)

    if not x:
        if VERBOSE:
            print(f"\t\t\t\t\t\t online \t offline ")
            print(f"{org['registers'] == registers} \tregisters\t\t {org['registers']} \t {registers} ")
            print(f"{org['pc'] == pc} \tpc\t\t\t\t {org['pc']} \t\t\t {pc} ")
            print(f"{org['pc_dir'] == pc_dir} \tpc_dir\t\t\t {org['pc_dir']} \t\t\t {pc_dir} ")
            print(f"{org['step'] == step} \tstep\t\t\t {org['step']} \t\t\t {step} ")
            print(f"{org['unused_breaks'] == unused_breaks} \tunused_breaks\t {org['unused_breaks']} \t\t {unused_breaks} ")
            print(f"{org['used_breaks'] == used_breaks} \tused_breaks\t\t {org['used_breaks']} \t\t {used_breaks} ")
            print(f"{org['cur_reg'] == cur_reg} \tcur_reg\t\t\t {org['cur_reg']} \t\t\t {cur_reg} ")
            print(f"{org['prev_reg'] == prev_reg} \tprev_reg\t\t {org['prev_reg']} \t\t\t {prev_reg} ")
            print(f"{org['reg_dir'] == reg_dir} \treg_dir\t\t\t {org['reg_dir']} \t\t\t {reg_dir} ")
            print(f"{org['steps_per_reg'] == steps_per_reg} \tsteps_per_reg\t {org['steps_per_reg']} \t {steps_per_reg} ")
            print(f"{org['cur_reg_steps'] == cur_reg_steps} \tcur_reg_steps\t {org['cur_reg_steps']} \t\t\t {cur_reg_steps}")
        else:
            print('WRONG  : ', end='')
            if org['registers'] != registers:
                SUPERWRONG.append(program)
                print(f"{program} - registers = {org['registers']} :: {registers}")
            else:
                WRONG.append(program)
                print(f"{program}")
    else:
        print(f"Success: {program}")




def get_reg(app_cur_reg, reg_dir, steps_per_reg):
    app_cur_reg += reg_dir
    if app_cur_reg == -1:
        app_cur_reg = sum(steps_per_reg) - 1
    app_cur_reg %= sum(steps_per_reg)
    cur_reg = 0
    con_steps_p_reg = 0
    for j in range(0, len(steps_per_reg)):
        pre_con_steps_p_reg = con_steps_p_reg
        con_steps_p_reg += steps_per_reg[j]
        if app_cur_reg - con_steps_p_reg < 0 <= app_cur_reg - pre_con_steps_p_reg:
            cur_reg = j
    return app_cur_reg, cur_reg


if __name__ == "__main__":
    main()
