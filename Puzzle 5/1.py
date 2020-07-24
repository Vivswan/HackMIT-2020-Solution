# -*- coding: utf-8 -*-
import itertools
import math

import requests
import re
import json

VERBOSE = True
SEARCH = False
STOPSEARCH = False
OFFW = []
WRONG = []
SUPERWRONG = []

# all_char = ''.join(['y', 'f', 's', '+', '-', 'c', 'b', 'a'])
arr_char = ['y', '+', 'b', 'a', 'c']
arr_char.reverse()
all_char = ''.join(arr_char)
all_char_reg_ex = all_char.replace('-', '\-')

pattern = re.compile("^[\+\-scb]+[" + all_char_reg_ex + "]*(b[" + all_char_reg_ex + "]+a)*[" + all_char_reg_ex + "]*$")
print(pattern.pattern)

XXXX = 0

def generate_strings(length=12):
    global pattern, all_char, XXXX
    for item in itertools.product(all_char, repeat=length):
        i = "".join(item)
        if re.search(pattern, i) is not None:
            XXXX += 1
            if XXXX % 1000000 == 0:
                print(f"{i} :: {XXXX}/{math.pow(len(arr_char), length)} : {XXXX * 100 / math.pow(len(arr_char), length)}")
            if i.__contains__('c') and i.__contains__('b') and i.__contains__('y') and i.__contains__('+'):
                yield i


# noinspection DuplicatedCode
def online(prog):
    url = 'https://zoomlang.hackmit.academy/api/interpret'
    data = {
        'username': "Vivswan_f17f03",
        'puzzlenum': "1",
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


def main():
    global VERBOSE, SEARCH, STOPSEARCH

    VERBOSE = False
    SEARCH = True
    for i in generate_strings():
    # for i in WRONG:
    # for i in OFFW:
        try:
            run(i)
        except:
            pass
        if SEARCH and STOPSEARCH:
            break
    print(WRONG)
    print(SUPERWRONG)
    print(OFFW)

    # VERBOSE = False
    # run('c+')
    # run('c++')
    # run('c+++')
    # VERBOSE = True
    # run('c+c++')


def run(program):
    global VERBOSE, SEARCH, STOPSEARCH

    if VERBOSE:
        print()
        print(program)

    org = None

    registers = [0, 0]

    pc = 0
    pc_dir = 1
    step = 0
    unused_breaks = []
    used_breaks = []
    cur_reg = 0
    prev_reg = None
    reg_dir = 1
    steps_per_reg = [1, 1]
    cur_reg_steps = 0

    app_cur_reg = 0

    i = 0
    while i < len(program):

        if VERBOSE and not SEARCH:
            print(f"{step} : {app_cur_reg} : {cur_reg} : {i} : {program[i]} : {steps_per_reg} : {used_breaks} : {unused_breaks} -- {registers}")

        if program[i] == "y":
            registers[cur_reg] += registers[prev_reg]

        if program[i] == "s":
            steps_per_reg[cur_reg] += 1

        if program[i] == "f":
            if steps_per_reg[cur_reg] <= 1:
                raise ValueError()
            steps_per_reg[cur_reg] -= 1
            t = 0
            for j in range(0, cur_reg + 1):
                t += steps_per_reg[j]
            app_cur_reg = t - reg_dir

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
            used_breaks.insert(0, i)
            # continue

        app_cur_reg, n_cur_reg = get_reg(app_cur_reg, reg_dir, steps_per_reg)

        if n_cur_reg != cur_reg:
            prev_reg = cur_reg
            cur_reg = n_cur_reg

        if prev_reg == cur_reg:
            cur_reg_steps += 1
        else:
            cur_reg_steps = 0

        i += 1
        step += 1

    if VERBOSE and not SEARCH:
        print(f"{step} : {app_cur_reg} : {cur_reg} : {i} :   : {steps_per_reg} : {used_breaks} : {unused_breaks} -- {registers}")

    pc = i

    if not SEARCH:
        try:
            org = online(program)
        except:
            OFFW.append(program)
            print(f"offline problem: {program}")
            return

        print_result(program, cur_reg, cur_reg_steps, org, pc, pc_dir, prev_reg, reg_dir, registers, step, steps_per_reg, unused_breaks, used_breaks)
    else:
        if not VERBOSE:
            if registers[0] >= 10000 and registers[1] >= 10000:
                r1 = registers[0] / registers[1]
                r2 = registers[1] / registers[0]
                precision = 0.00001
                if abs(r1 - 1.61803398875) < precision or abs(r2 - 1.61803398875) < precision:
                    result = online(program)
                    print(f"{result['registers'] == registers}, {result['flag']}, {result['msg']}, {program} --> {registers}, {r1}, {r2}")
                    if result['flag'] is not None:
                        STOPSEARCH = True


def print_result(program, cur_reg, cur_reg_steps, org, pc, pc_dir, prev_reg, reg_dir, registers, step,steps_per_reg, unused_breaks, used_breaks):
    global SEARCH, VERBOSE

    x = True
    x = x and (org['registers'] == registers)
    x = x and (org['pc'] == pc)
    x = x and (org['pc_dir'] == pc_dir)
    x = x and (org['step'] == step)
    x = x and (org['unused_breaks'] == unused_breaks)
    x = x and (org['used_breaks'] == used_breaks)
    x = x and (org['reg_dir'] == reg_dir)
    x = x and (org['steps_per_reg'] == steps_per_reg)
    if program[-1] == 's' and  program[-1] == 'f':
        x = x and (org['cur_reg'] == cur_reg)
        x = x and (org['prev_reg'] == prev_reg)
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
