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

    def get_days_activity(self, date: str):
        if date not in self.login_days_tracker:
            self.login_days_tracker[date] = BitMap()
        return self.login_days_tracker[date]

    def track_login_activity(self, user_id: int):
        date = get_date_str()
        self.get_days_activity(date).add(user_id)

    def active_users_count(self, activity: BitMap) -> int:
        return len(activity)

    def agg_activities(self, activities: List[BitMap]) -> BitMap:
        return BitMap.union(*activities)

    def get_inactive_users_count_for_a_week(self, total_users) -> int:
        days_in_week = get_past_week_days()
        activities = [self.get_days_activity(day) for day in days_in_week]
        return total_users - self.active_users_count(self.agg_activities(activities))

        # activity = BitMap()
        # for date in days_in_week:
        #     activity |= self.login_days_tracker.get(date, BitMap())
        # return total_users - self.active_users_count(activity)


if __name__ == '__main__':
    days_tracker = {}
    sess = SessionManager(days_tracker)
    for i in range(100000):
        sess.login(i)
    # print(sess.active_users_count(get_date_str()))
    print(sess.get_inactive_users_count_for_a_week(150000))
