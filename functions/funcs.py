import json
import os
import random
from collections import defaultdict
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

async def total_time_user(userId): #integration test in inttests
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

async def total_time_avg(userId): #integration test in inttests
    res = await total_time_user(userId)
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

async def post_metrics(userIdstr, data, reportname):
    res = await total_time_user(userIdstr)
    prevres = await total_time_avg(res)
    prevres['usersIds'] = data.users
    if 'dailyAverage' and 'weeklyAverage' in data.metrics:
        uid = str(uuid.uuid4())

        line_count = 0

        with open(reportname + ".txt", 'r') as existing_file:
            line_count = sum(1 for line in existing_file)

        if line_count == 0:
            return {"err": "invalid report name"}

        new_timestamp = int(datetime.now().timestamp() + 10800 + line_count * 86400)

        doc = {"uuid": uid, "timestamp": new_timestamp, "data": prevres}

        with open(reportname + ".txt", 'a') as file:
            json.dump(doc, file)
            file.write('\n')

        return {}

def calculate_metrics_result(user_appearances, daily_sum, daily_count, weekly_sum, weekly_count, reslist):
    resoutput = []

    for user_id in user_appearances:
        avg_daily = daily_sum[user_id] / daily_count[user_id]
        avg_weekly = weekly_sum[user_id] / weekly_count[user_id]
        total_time = avg_daily * user_appearances[user_id]

        user_metrics = {
            "userId": user_id,
            "metrics": [
                {"dailyAverage": avg_daily},
                {"weeklyAverage": avg_weekly},
                {"total": total_time},
                {"min": min(reslist, key=lambda x: x[1])[1]},
                {"max": max(reslist, key=lambda x: x[1])[1]}
            ]
        }

        resoutput.append(user_metrics)

async def get_reports(reportname, ffrom, to):
    line_count = 0

    try:
        tsfrom = int(datetime.fromisoformat(transform_to_iso_format(ffrom)).timestamp()+10800)
        tsto = int(datetime.fromisoformat(transform_to_iso_format(to)).timestamp()+10800)
    except:
        return {"err": "wrong time format"}

    try:
        with open(reportname + ".txt", 'r') as existing_file:
            line_count = sum(1 for line in existing_file)
    except:
        return {"err": "invalid report name"}

    if line_count == 0:
        return {"err": "invalid report name"}

    try:
        with open(reportname + ".txt", 'r') as file:
            data = [json.loads(line) for line in file if line.strip()]
    except:
        return {"err": "load failed"}

    if (tsto-tsfrom) % 86400 != 0:
        return {"err": "specify interval dividable on 24 hr"}

    reslist = []

    for entry in data:
        if tsfrom <= entry['timestamp'] <= tsto:
            user_ids = entry['data']['usersIds']
            daily_averages = entry['data']['dailyAverage']
            weekly_averages = entry['data']['weeklyAverage']

            for i, user_id in enumerate(user_ids):
                user_daily_avg = daily_averages[i]
                user_weekly_avg = weekly_averages[i]

                reslist.append([user_id, user_daily_avg, user_weekly_avg])

    daily_sum = defaultdict(float)
    daily_count = defaultdict(int)
    weekly_sum = defaultdict(float)
    weekly_count = defaultdict(int)

    user_appearances = defaultdict(int)

    for user_id, daily_avg, weekly_avg in reslist:
        daily_sum[user_id] += daily_avg
        daily_count[user_id] += 1
        weekly_sum[user_id] += weekly_avg
        weekly_count[user_id] += 1
        user_appearances[user_id] += 1

    user_averages = {}
    user_totals = {}

    for user_id in user_appearances:
        avg_daily = daily_sum[user_id] / daily_count[user_id]
        avg_weekly = weekly_sum[user_id] / weekly_count[user_id]
        total_time = avg_daily * user_appearances[user_id]

        user_averages[user_id] = {
            'averageDailyAverage': avg_daily,
            'averageWeeklyAverage': avg_weekly
        }
        user_totals[user_id] = total_time

    return calculate_metrics_result(user_appearances, daily_sum, daily_count, weekly_sum, weekly_count, reslist)