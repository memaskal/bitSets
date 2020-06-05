from datetime import datetime, timedelta
from typing import List


def get_date_str(timestamp=datetime.utcnow()) -> str:
    return timestamp.strftime("%Y-%m-%d")


def get_past_week_days() -> List[str]:
    today = datetime.utcnow()
    days = [today - timedelta(days=d) for d in range(6, -1, -1)]
    return list(map(get_date_str, days))
