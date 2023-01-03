from requests import get
from itertools import accumulate
import time
import json
import os
import sys

type = 'short'
media_id = sys.argv[1]
base_url = f'https://api.bilibili.com/pgc/review/{type}/list?media_id={media_id}&ps=20&sort=0'
result = {
    'short': [0, 0, 0, 0, 0, 0],
    'long': [0, 0, 0, 0, 0, 0]
}
next = 0

if sys.platform == 'win32':
    clear = lambda: os.system('cls')
elif sys.platform == 'linux':
    clear = lambda: os.system('clear')

def average(v):
    return sum(accumulate(v[:0:-1])) * 2 / sum(v)

def average_(v):
    return (v[2] * 4 + v[3] * 6 + v[4] * 8 + v[5] * 10) / sum(v[2:])

def run(cursor):
    res = json.loads(get(f'{base_url}&cursor={cursor}').text)['data']
    for i in res['list']:
        # if i['score'] == 0:
        #     print(i)
        #     input()
        result[type][i['score'] // 2] += 1
    clear()
    time.sleep(0)
    for k, v in result.items():
        print(f'{"长" if k == "long" else "短"}评:')
        for s, i in enumerate(v):
            print(f'    打{s}星的人数: {i}')
        if sum(v) != 0:
            print('    平均分:', average(v))
            print('    平均分(不包括1星)', average_(v))
        print('    人数:', sum(v))
    total = [a + b for a, b in zip(*result.values())]
    print('总平均分:', average(total))
    print('总平均分(不包括1星)', average_(total))
    print('总人数:', sum(total))
    if sum(result[type]) >= res['total']:
        return False
    global next
    next = res['next']
    return True

def start():
    global next, type, base_url
    while True:
        if not run(next):
            if type == 'short':
                type = 'long'
                base_url = f'https://api.bilibili.com/pgc/review/{type}/list?media_id={media_id}&ps=20&sort=0'
                next = 0
            else:
                print('结束')
                break

if __name__ == '__main__':
    start()

