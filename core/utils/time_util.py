from datetime import datetime, timezone, time


def getUtcSecond(hour: int = 0, minute: int = 0, second: int = 0):
    today_utc = datetime.now(timezone.utc).date()
    midnight_utc = datetime.combine(today_utc, time(hour, minute, second), timezone.utc)
    timestamp_utc = int(midnight_utc.timestamp())
    return timestamp_utc