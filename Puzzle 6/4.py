import requests

url = 'https://lockdown.hackmit.academy/api/Vivswan_1f372a'
filename = '4.asm'

file = open(filename, 'r')
text = file.read()
file.close()

run_result = None


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


def execute_run(multipler):
    global run_result
    run_result = requests.post(f"{url}/run", json={
        'code': text.replace('&&', str(multipler))
    }).json()

    if len(run_result['error']) > 0:
        print(run_result['error'])
        run_result = None
        return None

    run_result = parse_execution(run_result)
    return run_result


index = 0
while True:
    ans = execute_run(index)['regs'][18]
    ans = int(ans[ans.find('=') + 1:].strip())
    if ans == 0:
        break
    ans = chr(ans)
    print(ans, end="")
    index += 1
