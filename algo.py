from fastapi import FastAPI

from functions.funcs import hist_data, user_hist_data, predict_users, predict_user, total_time_user, total_time_avg, \
    gdprf, post_metrics, get_reports
from functions.utils import transform_metrics_list
from models import InputData

app = FastAPI()

async def gdpr(userId):
    await gdprf(userId)
    return {"msg": "added succesfully"}

@app.get('/api/stats/users')
async def get_users_historical_data(date: str):
    if not date:
        return {"usersOnline": None}

    return await hist_data(date)

@app.get('/api/stats/user')
async def get_user_historical_data(date: str, userId: str):
    if not date or not userId:
        return {"wasUserOnline": None, "nearestOnlineTime": None}

    return await user_hist_data(date, userId)

@app.get('/api/predictions/users')
async def predict_users_online(date: str):
    if not date:
        return {"OnlineUsers": None}

    return await predict_users(date)

@app.get('/api/predictions/user')
async def predict_user_online(date: str, tolerance: float, userId: str):
    if not date or not userId:
        return {"willBeOnline": None, "onlineChance": None}

    return await predict_user(date,tolerance,userId)

@app.get("/api/stats/user/total")
async def totalTime(userId: str):
    if not userId:
        return {"totalTime": None}

    userList = userId.split(',')

    return await total_time_user(userList)

@app.get("/api/stats/user/total/avg")
async def totalTimeAvg(userId):
    if not userId:
        return {"totalTime": None}

    return await total_time_avg(userId)

@app.post("/api/report/")
async def post_report(report_name: str, data: InputData):
    if data is None:
        return {"err": "empty response"}
    userIdstr = ",".join(data.users)
    return await post_metrics(userIdstr,data,report_name)

@app.get("/api/report/")
async def get_report(report_name: str, ffrom: str, to: str, ver: int): #version 1-old, 2-global
    if report_name is None or ffrom is None or to is None:
        return {"err": "not enough data"}

    if ver == 1:
        return await get_reports(report_name, ffrom, to)

    elif ver == 2:
        res = await get_reports(report_name, ffrom, to)
        return transform_metrics_list(res)

    elif ver == 3:
        res = await get_reports(report_name, ffrom, to)
        x = transform_metrics_list(res)
        return {"name": "dummy", "data": x}

@app.post('/api/user/forget')
async def forget_gdpr(userId: str):
    if not userId:
        return {"err": "missing id"}

    return await gdprf(userId)