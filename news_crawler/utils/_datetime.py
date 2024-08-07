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
    """
    datetime_to_date_string 將datetime依照format 輸出date_string

    Args:
        datetime (datetime): datetime obj
        format (str): 日期格式

    Returns:
        str: 日期格式字串
    """
    return datetime.strftime(format)


def datetime_to_iso_date_string(datetime: datetime) -> str:
    """
    datetime_to_iso_date_string 將datetime 輸出成iso format格式的日期字串

    Args:
        datetime (datetime): datetime obj

    Returns:
        str: iso format格式的日期字串
    """
    return datetime.isoformat()


def iso_date_string_to_datetime(iso_date_string: str) -> datetime:
    """
    iso_date_string_to_datetime iso format格式的日期字串輸出成datetime obj

    Args:
        iso_date_string (str): iso format格式的日期字串

    Returns:
        datetime: datetime obj
    """
    return datetime.fromisoformat(iso_date_string)
