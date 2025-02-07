from datetime import datetime


def time_diff_in_seconds(start: datetime, end: datetime) -> int:
    return int(end.timestamp() - start.timestamp())
