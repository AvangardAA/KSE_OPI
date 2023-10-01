import requests
from datetime import datetime, timedelta
api_url = "https://sef.podkolzin.consulting/api/users/lastSeen"
def fetch(offset):
    response = requests.get(f"{api_url}?offset={offset}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed offset: {offset}")
        return []

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

def normalize_time(last_seen_date, locale):
    if not last_seen_date:
        return dictionary[locale]['thxfor3amcoding']

    now = datetime.utcnow()

    date_str = last_seen_date[:10]
    time_str = last_seen_date[11:19]

    fracsec = 0
    if '.' in last_seen_date:
        fracsecstr = last_seen_date.split('.')[1]
        if fracsecstr.isdigit():
            fracsec = int(fracsecstr)

    try:
        date_time = datetime.strptime(date_str + ' ' + time_str, "%Y-%m-%d %H:%M:%S")
        date_time += timedelta(microseconds=fracsec)
    except ValueError:
        return dictionary[locale]['unreal_to_parse']

    difference = now - date_time

    if difference < timedelta(seconds=30):
        return dictionary[locale]['now']
    elif difference < timedelta(seconds=60):
        return dictionary[locale]['last_min']
    elif difference < timedelta(minutes=59):
        return dictionary[locale]['less_than_hour_minutes']
    elif difference < timedelta(minutes=119):
        return dictionary[locale]['hour_ago']
    elif difference < timedelta(hours=24):
        return dictionary[locale]['today']
    elif timedelta(hours=24):
        return dictionary[locale]['yesterday']
    elif difference < timedelta(days=7):
        return dictionary[locale]['week']
    else:
        return dictionary[locale]['sleeping']