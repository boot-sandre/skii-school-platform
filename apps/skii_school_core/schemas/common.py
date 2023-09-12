from datetime import datetime, timedelta
from typing import List, Any

from ninja import Schema


class TimeRange(Schema):
    start: datetime
    stop: datetime
    delta: timedelta
