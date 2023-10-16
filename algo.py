from fastapi import FastAPI

from functions.funcs import hist_data, user_hist_data, predict_users, predict_user, total_time_user, total_time_avg, \
    gdprf, post_metrics
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

    res = await total_time_user(userId)
    return await total_time_avg(res)

@app.post("/api/report/")
async def post_report(report_name: str, data: InputData):
    if data is None:
        return {"err": "empty response"}
    userIdstr = ",".join(data.users)
    res = await total_time_user(userIdstr)
    res = await total_time_avg(res)
    res['usersIds'] = data.users
    return await post_metrics(data.metrics, res, report_name)

@app.post('/api/user/forget')
async def forget_gdpr(userId: str):
    if not userId:
        return {"err": "missing id"}

    return await gdpr(userId)