import requests

url = 'https://lockdown.hackmit.academy/api/Vivswan_1f372a'
filename = '4.asm'

file = open(filename, 'r')
lines = file.readlines()
file.close()

filtered_lines = []
run_result = None

for i in range(0, len(lines)):
    if len(lines[i][0: lines[i].strip().find('#')].strip()) > 0:
        filtered_lines.append(lines[i].replace('\n', ''))


def parse_execution(param):
    xx = param['regs'].split('\n')
    yy = []
    max_length = 0
    for i in xx:
        zz = i[i.find('=') + 1:].strip()
        aa = zz + " = " + str(int(zz[zz.find('x') + 1:], 16))
        yy.append(aa)
        if len(aa) > max_length:
            max_length = len(aa)

    param['regs'] = yy
    param['regs_length'] = max_length
    return param


def execute_run():
    global run_result
    run_result = requests.post(f"{url}/run", json={
        'code': '\n'.join(filtered_lines)
    }).json()

    if len(run_result['error']) > 0:
        print(run_result['error'])
        run_result = None
        return None

    run_result = parse_execution(run_result)
    return run_result


def print_run():
    run_result = execute_run()

    if run_result is None:
        return None

    arr_regs = run_result['regs']
    for reg_index in range(0, len(arr_regs)):
        print(f'r{reg_index}' + ' ' * (3 - len(str(reg_index))) + '= ', end='')

        if arr_regs[reg_index] == '0x00000000 = 0':
            print(' ' * run_result['regs_length'], end='')
        else:
            print(arr_regs[reg_index] + (' ' * (run_result['regs_length'] - len(arr_regs[reg_index]))), end='')

        print(end='\t')
        if (reg_index + 1) % 3 == 0:
            print()

    print()


def execute_steps():
    executions = []
    line_number = 1
    while True:
        execution = requests.post(f"{url}/step/{line_number}", json={
            'code': '\n'.join(filtered_lines),
            'step': line_number
        }).json()

        if len(execution['error']) > 0:
            print(execution['error'])
            return None

        executions.append({
            'step': line_number,
            'line': execution['instruction'],
            'execution': parse_execution(execution)
        })
        line_number += 1
        if len(executions) > 3:
            if executions[-1]['line'] == executions[-2]['line'] and executions[-2]['line'] == executions[-3]['line']:
                break

    return executions[:-2]


def print_steps():
    steps = execute_steps()
    if steps is None:
        return None

    max_step_length = 0
    for step in steps:
        max_step_length = max(max_step_length, len(step['line']))
    max_step_length += 4

    reg_exclusions = []
    for reg_exc_index in range(0, 32):
        c = True
        for step_index in range(0, len(steps)):
            if steps[step_index]['execution']['regs'][reg_exc_index] != '0x00000000':
                c = False
                break
        if c:
            reg_exclusions.append(reg_exc_index)

    print(' ' * (4 + max_step_length), end='')
    for i in range(0, 32):
        if not reg_exclusions.__contains__(i):
            print(f'r{i}' + (' ' * (11 - len(f'r{i}'))), end='')
    print()

    for step_index in range(0, len(steps)):
        regs = ''
        arr_regs = steps[step_index]['execution']['regs']
        for reg_index in range(0, len(arr_regs)):
            if not reg_exclusions.__contains__(reg_index):
                if arr_regs[reg_index] == '0x00000000':
                    regs += ' ' * 11
                else:
                    regs += arr_regs[reg_index] + ' '

        print(
            str(steps[step_index]['step']) +
            ' ' * (4 - len(str(steps[step_index]['step']))) +
            steps[step_index]['line'] +
            ' ' * (max_step_length - len(steps[step_index]['line'])) +
            regs
        )

    return run_result


# print_steps()
# print()
print_run()
