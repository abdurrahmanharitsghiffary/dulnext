import datetime


def timestamp_to_frappe_date(num: int):
    try:
        return datetime.datetime.fromtimestamp(num / 1000)
    except Exception as e:
        return None
