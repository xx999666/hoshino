import requests
import json
import brotli
import time
import os
import sqlite3
from . import Service

from .campaign import parse_campaign

_resource_path = os.path.expanduser('~/.hoshino')


# 开辟一个数组来储存地址，依次是服务器数据库，服务器版本Json，本地数据库，本地版本Json
# bilibili
bili_url = 'https://redive.estertion.win/db/redive_cn.db.br'
bili_verurl = 'https://redive.estertion.win/last_version_cn.json'
bili_db = os.path.join(_resource_path, 'redive_bili.db')
bili_ver = os.path.join(_resource_path, 'bili_ver.json')
bililist = [bili_url, bili_verurl, bili_db, bili_ver]
# jp
jp_url = 'https://redive.estertion.win/db/redive_jp.db.br'
jp_verurl = 'https://redive.estertion.win/last_version_jp.json'
jp_db = os.path.join(_resource_path, 'redive_jp.db')
jp_ver = os.path.join(_resource_path, 'jp_ver.json')
jplist = [jp_url, jp_verurl, jp_db, jp_ver]


def updateDB(sv: Service, serid):
    if serid == 'jp':
        ls = jplist
    if serid == 'bili':
        ls = bililist
    ver_res = requests.get(ls[1])
    if ver_res.status_code != 200:
        sv.logger.warning('连接服务器失败')
        return
    ver_get = ver_res.content
    ver = json.loads(ver_get)
    ver_path = ls[3]
    db_res = requests.get(ls[0])
    if db_res.status_code != 200:
        sv.logger.warning('连接服务器失败')
        return
    data_get = db_res.content
    data = brotli.decompress(data_get)
    db_path = ls[2]
    with open(db_path, 'wb') as dbfile:
        dbfile.write(data)
        dbfile.close()
    with open(ver_path, 'w', encoding='utf8') as vfile:
        json.dump(ver, vfile, ensure_ascii=False)
        vfile.close()
    sv.logger.info(f'{serid}数据库更新成功')


def check_ver(sv: Service, serid):
    if serid == 'jp':
        ls = jplist
    if serid == 'bili':
        ls = bililist
    try:
        with open(ls[3], encoding='utf8') as vfile:
            local_ver = json.load(vfile)
    except FileNotFoundError as e:
        sv.logger.warning(f'未发现{serid}数据库,将会稍后创建')
        updateDB(sv, serid)
        return
    ver_res = requests.get(ls[1])
    if ver_res.status_code != 200:
        sv.logger.warning('连接服务器失败')
        return
    ver_get = ver_res.content
    online_ver = json.loads(ver_get)
    if local_ver == online_ver:
        sv.logger.info(f'未发现{serid}数据库更新')
        pass
    else:
        sv.logger.info(f'发现{serid}数据库更新,将会稍后更新')
        updateDB(sv, serid)


def campaign_logout(campaign, value):
    name = parse_campaign(campaign)
    if name is None:
        return None
    vlue = f'{int(value)/1000}倍'
    return name, vlue


def db_message(sv, serid, tense='all', lastday=7):
    if serid == 'bili':
        database_path = bililist[2]
        fmsg='B服日程'
    if serid == 'jp':
        database_path = jplist[2]
        fmsg='日服日程'
    if not os.path.exists(database_path):
        updateDB(sv, serid)
    db = sqlite3.connect(database_path)
    selectcampaign = '''
    SELECT campaign_category, value, start_time, end_time
    FROM campaign_schedule
    ORDER BY start_time'''
    selectevent = '''
    SELECT a.start_time, a.end_time, b.title
    FROM hatsune_schedule AS a JOIN event_story_data AS b ON a.event_id = b.value '''
    campaign_data = db.execute(selectcampaign)
    event_data = db.execute(selectevent)
    cmsg1 = '当前日程\n|区域|倍率|===开始时间===|===结束时间===|'
    cmsg2 = '预定日程\n|区域|倍率|===开始时间===|===结束时间===|'
    for cdata in campaign_data:
        e_time = time.strptime(cdata[3], '%Y/%m/%d %H:%M:%S')
        e_time_int = int(time.mktime(e_time))
        s_time = time.strptime(cdata[2], '%Y/%m/%d %H:%M:%S')
        s_time_int = int(time.mktime(s_time))
        localtime_int = int(time.time())
        now_data = campaign_logout(cdata[0], cdata[1])
        if now_data is None:
            continue
        name, value = ','.join(now_data).split(',')
        stime = time.strftime('%Y-%m-%d %H:%M:%S', s_time)
        etime = time.strftime('%Y-%m-%d %H:%M:%S', e_time)
        if localtime_int < e_time_int and localtime_int > s_time_int:
            cmsg1 += f'\n|{name}|{value}|{stime}|{etime}|'
        if s_time_int > localtime_int:
            if lastday != 0:
                if s_time_int > localtime_int+(84600*lastday):
                    continue
            cmsg2 += f'\n|{name}|{value}|{stime}|{etime}|'

    emsg1 = '====当前活动====='
    emsg2 = '====预定活动====='
    for edata in event_data:
        e_time = time.strptime(edata[1], '%Y/%m/%d %H:%M:%S')
        e_time_int = int(time.mktime(e_time))
        s_time = time.strptime(edata[0], '%Y/%m/%d %H:%M:%S')
        s_time_int = int(time.mktime(s_time))
        localtime_int = int(time.time())
        title = edata[2]
        stime = time.strftime('%Y-%m-%d %H:%M:%S', s_time)
        etime = time.strftime('%Y-%m-%d %H:%M:%S', e_time)
        if localtime_int < e_time_int and localtime_int > s_time_int:
            emsg1 += ('\n{}\n开始时间:{}\n结束时间:{}').format(
                title, stime, etime)
        if s_time_int > localtime_int:
            if lastday == 0:
                pass
            if lastday != 0:
                if s_time_int > localtime_int+(84600*lastday):
                    continue
            emsg2 += ('\n{}\n开始时间:{}\n结束时间:{}').format(
                title, stime, etime)

    if tense == 'all':
        fmsg += '\n'+cmsg1+'\n'+cmsg2+'\n'+emsg1+'\n'+emsg2
    if tense == 'future':
        fmsg += '\n'+cmsg2+'\n'+emsg2
    if tense == 'now':
        fmsg += '\n'+cmsg1+'\n'+emsg1
    return fmsg
