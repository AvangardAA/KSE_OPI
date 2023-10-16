import time
from datetime import datetime
import random
import requests

from functions.funcs import normalize_time_human_implementation, fetch
from functions.utils import transform_from_iso_format


def main():
    #print(check_dates_correspond("2025-27-09-20:00", "2025-14-09-20:00"))
    language = input("Choose language for response: english/ukrainian\n")
    #print(normalize_time_human_implementation("2023-10-11T20:29:33.8772757+00:00", language, "2023-11-10-20:00"))
    c = 0
    users_data = fetch(c)
    q = int(users_data['total'])
    while q > 0:
        #print(c)
        #print("\n")
        for user in users_data['data']:
            username = user["nickname"]
            status = normalize_time_human_implementation(user['lastSeenDate'], language)
            print(f"{username} {status}")
        q -= len(users_data['data'])
        c += len(users_data['data'])
        users_data = fetch(c)

def new():
    while True:
        resbuf = []
        idbuf = []
        res = requests.get("http://127.0.0.1:8000/api/stats/users", {"date": transform_from_iso_format(int(datetime.now().timestamp())+10800)})
        resbuf.append({"usersOnline": res.json()["usersOnline"]})
        idbuf = res.json()["users"]
        res = requests.get("http://127.0.0.1:8000/api/stats/user", {"date": transform_from_iso_format(int(datetime.now().timestamp())+10800), "userId": random.choice(idbuf)})
        resbuf.append(res.text)
        res = requests.get("http://127.0.0.1:8000/api/predictions/users",
                           {"date": transform_from_iso_format(int(datetime.now().timestamp()) + 10800)})
        resbuf.append(res.text)
        res = requests.get("http://127.0.0.1:8000/api/predictions/user",
                           {"date": transform_from_iso_format(int(datetime.now().timestamp()) + 10800), "userId": random.choice(idbuf), "tolerance": random.randint(30, 80)})
        resbuf.append(res.text)
        requests.post("http://127.0.0.1:8000/api/user/forget?userId=5a254c98-a749-ab02-bf62-2f9a4fb1e98a") #forget and block request to process
        res = requests.get("http://127.0.0.1:8000/api/stats/user",
                           {"date": transform_from_iso_format(int(datetime.now().timestamp()) + 10800),
                            "userId": "5a254c98-a749-ab02-bf62-2f9a4fb1e98a"}) #check if gpdr works
        resbuf.append(res.text)
        for i in resbuf:
            print(i)
        time.sleep(30)

def postcheck():
    url = "http://127.0.0.1:8000/api/report?report_name=dummy"
    data = {
        "metrics": ["dailyAverage", "weeklyAverage"],
        "users": ["e13412b2-fe46-7149-6593-e47043f39c91", "908dcb71-beeb-57c4-72f6-50451a6c3d12"]
    }

    response = requests.post(url, json=data)
    print(response.text)

if __name__ == "__main__":
    postcheck()
