from datetime import datetime

DEFAULT_TIME_PATTERN = "%Y-%m-%d %H:%M:%S"

def format_datetime(dt: datetime, fmt: str = DEFAULT_TIME_PATTERN) -> str:
    return dt.strftime(fmt)