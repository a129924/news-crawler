from datetime import datetime, tzinfo
from typing import Optional, Union


def timestamp_to_datetime(
    timestamp: Union[int, float], time_zone: Optional[tzinfo] = None
) -> datetime:
    """
    timestamp_to_datetime 輸入timestamp 輸出相對應的datetime

    Args:
        timestamp (int | float): 時間戳記
        time_zone (tzinfo | None, optional): 時區. Defaults to None.

    Returns:
        datetime: 相對應的datetime
    """
    return datetime.fromtimestamp(timestamp, tz=time_zone)


def datetime_to_date_string(datetime: datetime, format: str) -> str:
    return datetime.strftime(format)
