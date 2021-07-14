from datetime import datetime, timezone

def to_datetime(timestamp):
    return datetime.strptime(timestamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)