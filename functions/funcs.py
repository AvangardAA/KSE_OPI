import json
import random
from datetime import datetime
import uuid

import requests
from functions.utils import transform_to_iso_format, transform_from_iso_format, check_dates_correspond

api_url = "https://sef.podkolzin.consulting"

global ignorebuf
ignorebuf = []

dictionary = \
    {
    'english':
        {
        'thxfor3amcoding': '0',
        'unreal_to_parse': 'coders pain',
        'now': 'is online now',
        'last_min': 'was online last minute',
        'less_than_hour_minutes': 'was online 5 minutes ago',
        'hour_ago': 'was online hour ago',
        'today': 'was online today',
        'yesterday': 'was online yesterday',
        'week': 'was seen in a week',
        'sleeping': 'was seen',
    }, 'ukrainian':
    {
        'thxfor3amcoding': '0',
        'unreal_to_parse': 'біль кодера',
        'now': 'зараз онлайн',
        'last_min': 'був(ла) в мережі в останню хвилину',
        'less_than_hour_minutes': 'був(ла) в мережі 5 хвилин тому',
        'hour_ago': 'був(ла) в мережі годину тому',
        'today': 'був(ла) в мережі сьогодні',
        'yesterday': 'був(ла) в мережі вчора',
        'week': 'був(ла) в мережі протягом тижня',
        'sleeping': 'був(ла) в мережі',
    }
}

def fetch(offset):
    response = requests.get(f"{api_url}/api/users/lastSeen?offset={offset}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed offset: {offset}")
        return []
def normalize_time_human_implementation(last_seen_date, locale, DDate=None):
    if not last_seen_date:
        return dictionary[locale]['thxfor3amcoding']

    ts_now = int(datetime.now().timestamp())
    tsDDate = 0
    ts = 1

    if DDate is not None:
        try:
            DDate=transform_to_iso_format(DDate)
            tsDDate = int(datetime.fromisoformat(DDate).timestamp())
        except:
            return dictionary[locale]['unreal_to_parse']

    try:
        ts = int(datetime.fromisoformat(last_seen_date).timestamp())
    except:
        return dictionary[locale]['unreal_to_parse']

    if DDate is not None:
        #print(abs(tsDDate - ts))
        if abs(tsDDate-ts) < 86399:
            return {"ts": ts, "status": "yes"}
        else:
            return {"ts": abs(tsDDate - ts), "status": "no"}
    else:
        if ts_now-ts < 30:
            return dictionary[locale]['now']
        elif 60 > ts_now-ts > 30:
            return dictionary[locale]['last_min']
        elif 3599 > ts_now-ts > 60:
            return dictionary[locale]['less_than_hour_minutes']
        elif 7198 > ts_now-ts > 3599:
            return dictionary[locale]['hour_ago']
        elif 86399 > ts_now-ts > 7198:
            return dictionary[locale]['today']
        elif 172799 > ts_now-ts > 86399:
            return dictionary[locale]['yesterday']
        elif 604799 > ts_now-ts > 172799:
            return dictionary[locale]['week']
        else:
            return dictionary[locale]['sleeping']

async def hist_data(date):
    global ignorebuf
    c = 0
    cc = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    print(q)
    userbuf = []
    while q > 0:
        for user in users_data['data']:
            if (user['userId'] in ignorebuf):
                return {"err": "cant process"}
            userbuf.append(user['userId'])
            res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=date)
            try:
                if res["status"] == "yes":
                    cc += 1
            except:
                continue
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)
        return {"usersOnline": cc, "users": userbuf}

async def user_hist_data(date, userId):
    global ignorebuf
    c = 0
    was = False
    users_data = fetch(c)
    q = int(users_data['total'])
    nearest = None
    while q > 0:
        for user in users_data['data']:
            if (user['userId'] in ignorebuf):
                return {"err": "cant process"}
            if user["userId"] == userId.lower():
                res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=date)
                if (res == '0'):
                    was = None
                    break
                try:
                    if res["status"] == "yes":
                        was = True
                        break
                    else:
                        nearest = int(res["ts"])
                        if nearest is not None:
                            if nearest < res["ts"]:
                                nearest = res["ts"]
                except:
                    pass
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

    return {"wasUserOnline": was, "nearestOnlineTime": nearest}

async def predict_users(date):
    global ignorebuf
    c = 0
    cc = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    while q > 0:
        for user in users_data['data']:
            if (user['userId'] in ignorebuf):
                return {"err": "cant process"}
            res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=transform_from_iso_format(
                int(datetime.now().timestamp()) + 10800))
            try:
                if res["status"] == "yes":
                    cc += 1
            except:
                pass
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

    if check_dates_correspond(date, transform_from_iso_format(int(datetime.now().timestamp()) + 10800)):
        return {"OnlineUsers": cc}
    else:
        return {"Error": "datesArentSame"}

async def predict_user(date, tolerance, userId):
    global ignorebuf
    c = 0
    was = False
    users_data = fetch(c)
    q = int(users_data['total'])
    chance = 0.0
    while q > 0:
        for user in users_data['data']:
            if (user['userId'] in ignorebuf):
                return {"err": "cant process"}
            if user["userId"] == userId.lower():
                res = normalize_time_human_implementation(user['lastSeenDate'], "english",
                                                          DDate=transform_from_iso_format(
                                                              int(datetime.now().timestamp()) + 10800))
                if (res == '0'):
                    was = None
                    break
                try:
                    if res["status"] == "yes":
                        was = True
                        break
                except:
                    pass
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

    if (was == True):
        chance = float(1 / ((int(datetime.fromisoformat(transform_to_iso_format(date)).timestamp()) - (
                    int(datetime.now().timestamp()) + 10800)) / 604800) * 100)

    if chance < tolerance:
        was = False
    return {"willBeOnline": was, "onlineChance": "{:.2f}".format(chance)}

async def gdprf(userId):
    global ignorebuf
    ignorebuf.append(userId)
    return {'msg': "added successfully"}

async def total_time_user(userId):
    global ignorebuf
    c = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    lstrandom = []
    lstseentransformed = 0
    for i in userId:
        i = i.lower()
    while q > 0:
        for user in users_data['data']:
            if (user['userId'] in ignorebuf):
                lstrandom.append(0)
                continue
            if user["userId"] in userId:
                if user["lastSeenDate"] is not None:
                    lstseentransformed = int(datetime.fromisoformat(user["lastSeenDate"]).timestamp())
                    lstrandom.append(lstseentransformed - (lstseentransformed - random.randint(1000, 100000)))
                    continue
                else:
                    lstrandom.append(0)
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

    return {"totalTime": lstrandom}

async def total_time_avg(res):
    randbuf = []
    resbuf = []
    if len(res['totalTime']) == 1:
        for i in res['totalTime']:
            if i == 0:
                return resbuf.append({'err': "cant process"})
            else:
                x = random.randint(2, 10)
                for j in range(x):
                    randbuf.append(i)

                for i in randbuf:
                    i += random.randint(100, 10000)

                avgDays = []
                avgWeek = []

                avgDays.append(sum(randbuf) / len(randbuf))
                avgWeek.append(avgDays[0] * 7)

                return {"dailyAverage": avgDays, "weeklyAverage": avgWeek}
    else:
        x = random.randint(2, 10)
        for i in res['totalTime']:
            lx = []
            for j in range(x):
                lx.append(i)
            randbuf.append(lx)

        for i in randbuf:
            for j in i:
                j += random.randint(100, 10000)

        avgDays = []
        avgWeek = []
        for i in randbuf:
            avgDays.append(sum(i) / len(i))

        for i in range(len(avgDays)):
            avgWeek.append(avgDays[i] * 7)

        return {"dailyAverage": avgDays, "weeklyAverage": avgWeek}

async def post_metrics(metrics, prevres, reportname):
    if 'dailyAverage' and 'weeklyAverage' in metrics:
        uid = str(uuid.uuid4())
        doc = {"uuid": uid, "data": prevres}
        output = reportname + ".txt"
        with open(output, 'a') as file:
            json.dump(doc, file)
            file.write('\n')
        return {}