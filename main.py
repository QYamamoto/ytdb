from requests import get
from itertools import accumulate
from rich.table import Table
from rich.console import Console
import time
import json
import os
import sys

type = 'long'
media_id = sys.argv[1]
sort = 0 if len(sys.argv) <= 2 else int(sys.argv[2])
base_url = f'https://api.bilibili.com/pgc/review/{type}/list?media_id={media_id}&ps=20&sort={sort}'
result = {
    'short': [0, 0, 0, 0, 0, 0],
    'long': [0, 0, 0, 0, 0, 0]
}
next = 0
cons = Console()

if sys.platform == 'win32':
    clear = lambda: os.system('cls')
elif sys.platform == 'linux':
    clear = lambda: os.system('clear')

def average(v):
    return sum(accumulate(v[:0:-1])) * 2 / sum(v)

def average_(v):
    return (v[2] * 4 + v[3] * 6 + v[4] * 8 + v[5] * 10) / sum(v[2:])

def run(cursor):
    time.sleep(0)
    res = json.loads(get(f'{base_url}&cursor={cursor}').text)['data']
    ctime = 0
    for i in res['list']:
        # if i['score'] == 0:
        #     print(i)
        #     input()
        result[type][i['score'] // 2] += 1
        ctime = i['ctime']
    cons.clear()
    scores = Table('类型', *map(lambda x: f'{x}星', range(6)), '平均分', '平均分(去掉1星)', '人数', title='评分')
    for k, v in result.items():
        scores.add_row(
            f'{"长" if k == "long" else "短"}评',
            *map(str, v),
            *map(lambda x: f'[red]{round(x, 4)}[/red]', (average(v), average_(v)) if sum(v) else (0, 0)),
            f'[red]{sum(v)}[/red]'
        )
    cons.print(scores)
    if sort:
        print('当前时间:', time.ctime(ctime))
    total = [a + b for a, b in zip(*result.values())]
    cons.print(f'[i]总平均分[i]: [red]{average(total)}[/red]')
    cons.print(f'[i]总平均分(不包括1星)[i]: [red]{average_(total)}[/red]')
    cons.print(f'[i]总人数[i]: [red]{sum(total)}[/red]')
    if sum(result[type]) >= res['total']:
        return False
    global next
    next = res['next']
    return True

def start():
    global next, type, base_url
    while True:
        if not run(next):
            if type == 'long':
                type = 'short'
                base_url = f'https://api.bilibili.com/pgc/review/{type}/list?media_id={media_id}&ps=20&sort={sort}'
                next = 0
            else:
                cons.print('[u]结束[/u]')
                break

if __name__ == '__main__':
    start()

