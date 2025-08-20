from __future__ import annotations
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def to_utc_from_ist(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = IST.localize(dt)
    return dt.astimezone(pytz.UTC)

def convert_utc_to_tz(dt_utc: datetime, tz_name: str | None) -> datetime:
    tz = pytz.timezone(tz_name) if tz_name else IST
    return dt_utc.astimezone(tz)
