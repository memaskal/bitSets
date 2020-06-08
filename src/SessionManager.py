from typing import Dict
from pyroaring import BitMap
from src.utils import *


class SessionManager:
    def __init__(self, login_days_tracker: Dict[str, BitMap]):
        self.login_days_tracker = login_days_tracker

    def login(self, user_id: int):
        # do login related stuff
        # upon success track user activity
        self.track_login_activity(user_id)

    def get_days_activity(self, date: str) -> BitMap:
        if date not in self.login_days_tracker:
            self.login_days_tracker[date] = BitMap()
        return self.login_days_tracker[date]

    def track_login_activity(self, user_id: int):
        date = get_date_str()
        self.get_days_activity(date).add(user_id)

    @staticmethod
    def active_users_count(activity: BitMap) -> int:
        return len(activity)

    @staticmethod
    def agg_activities(activities: List[BitMap]) -> BitMap:
        return BitMap.union(*activities)

    def get_inactive_users_count_for_a_week(self, total_users) -> int:
        days_in_week = get_past_week_days()
        activities = [self.get_days_activity(day) for day in days_in_week]
        return total_users - self.active_users_count(self.agg_activities(activities))
