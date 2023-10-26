from datetime import datetime


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

def make_res_list(data, tsfrom, tsto):
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

    return reslist