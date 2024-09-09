import requests
from datetime import datetime, timedelta

def _get_target_time():
    tn = datetime.now()
    return datetime(tn.year, tn.month, tn.day, tn.hour, 30, 0)

def _as_datetime(txt):
    return datetime.strptime(txt, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=9)

server_list = ['전섭', '루페온', '실리안', '아만', '아브렐슈드', '카단', '카마인', '카제로스', '니나브']

async def merchant(server):
    if server not in server_list: return [] # '존재하지 않는 서버입니다.'
    url = 'https://api.korlark.com/merchants?limit=15'

    _target_time = _get_target_time()

    server_param = '&server=%s'%server_list.index(server) if server != '전섭' else ''
    merchants = await requests.get(url+server_param).json()['merchants']

    return [{
        'server': server_list[d['server']],
        'area': '%s, %s'%(d['continent'], d['zone']),
        'card': d['card'],
        'extra': d['extra'] if d['extra'] else '',
        'user': d['user']['stove']['nickname'],
        'time': _target_time.strftime('%H:%M'),
    } for d in merchants if _as_datetime(d['created_at']) > _target_time]

# [{'server': '카단',
#   'area': '욘, 무쇠망치 작업장',
#   'card': '피에르 카드',
#   'extra': '',
#   'user': '도깨비놀이터', 
#   'time': '10:30'},
#  {'server': '카단',
#   'area': '베른 북부, 크로나 항구',
#   'card': '기드온 카드',
#   'extra': '',
#   'user': '도핑샤프롱', 
#   'time': '10:30'}, ...]

# from crawler.merchant import merchant
# @app.command()
# async def 떠상(ctx, *, server:str):
#     result = await merchant(server)
#     # 데이터 처리

#     embed=discord.Embed()
#     # ??

#     await ctx.send(embed=embed)

