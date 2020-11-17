from datetime import datetime

def to_datetime(timestamp):
    return datetime.strptime(timestamp, "%Y%m%d%H%M%S")