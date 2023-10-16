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