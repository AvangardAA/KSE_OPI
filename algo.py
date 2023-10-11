from fastapi import FastAPI
import requests
from datetime import datetime
api_url = "https://sef.podkolzin.consulting"
app = FastAPI()
def fetch(offset):
    response = requests.get(f"{api_url}/api/users/lastSeen?offset={offset}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed offset: {offset}")
        return []

def transform_to_iso_format(date):
    try:
        input = datetime.strptime(date, '%Y-%d-%m-%H:%M')
        iso = input.isoformat()
        return iso
    except ValueError:
        return "format error"

def transform_from_iso_format(ts):
    try:
        dt = datetime.utcfromtimestamp(ts)
        formatt = dt.strftime('%Y-%d-%m-%H:%M')
        return formatt
    except ValueError:
        return "ts error"

def check_dates_correspond(date1, date2):
    try:
        dt1 = datetime.strptime(date1, '%Y-%d-%m-%H:%M')
        dt2 = datetime.strptime(date2, '%Y-%d-%m-%H:%M')

        if (dt1.weekday() == dt2.weekday()) and (dt1.time() == dt2.time()):
            return True
        else:
            return False
    except ValueError:
        return "format error"

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

@app.get('/api/stats/users')
async def get_users_historical_data(date: str):
    if not date:
        return {"usersOnline": None}

    c = 0
    cc = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    while q > 0:
        for user in users_data['data']:
            res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=date)
            try:
                if res["status"]=="yes":
                    cc += 1
            except:
                pass
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

    return {"usersOnline": cc}

@app.get('/api/stats/user')
async def get_user_historical_data(date: str, userId: str):
    if not date or not userId:
        return {"wasUserOnline": None, "nearestOnlineTime": None}

    c = 0
    was = False
    users_data = fetch(c)
    q = int(users_data['total'])
    nearest = None
    while q > 0:
        for user in users_data['data']:
            if user["userId"] == userId.lower():
                res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=date)
                if (res=='0'):
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

@app.get('/api/predictions/users')
async def predict_users_online(date: str):
    if not date:
        return {"OnlineUsers": None}

    c = 0
    cc = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    while q > 0:
        for user in users_data['data']:
            res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=transform_from_iso_format(int(datetime.now().timestamp())+10800))
            try:
                if res["status"]=="yes":
                    cc += 1
            except:
                pass
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

    if check_dates_correspond(date, transform_from_iso_format(int(datetime.now().timestamp())+10800)):
        return {"OnlineUsers": cc}
    else:
        return {"Error": "datesArentSame"}

@app.get('/api/predictions/user')
async def predict_user_online(date: str, tolerance: float, userId: str):
    if not date or not userId:
        return {"willBeOnline": None, "onlineChance": None}

    c = 0
    was = False
    users_data = fetch(c)
    q = int(users_data['total'])
    chance = 0.0
    while q > 0:
        for user in users_data['data']:
            if user["userId"] == userId.lower():
                res = normalize_time_human_implementation(user['lastSeenDate'], "english", DDate=transform_from_iso_format(int(datetime.now().timestamp())+10800))
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

    if (was==True):
        chance = float(1 / ((int(datetime.fromisoformat(transform_to_iso_format(date)).timestamp())-(int(datetime.now().timestamp())+10800))/604800)*100)

    if chance < tolerance:
        was = False
    return {"willBeOnline": was, "onlineChance": "{:.2f}".format(chance)}