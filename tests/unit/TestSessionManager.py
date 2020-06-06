import unittest
from typing import List
from src.utils import get_date_str
from src.SessionManager import SessionManager
from datetime import datetime, timedelta


class TestSessionManager(unittest.TestCase):
    def setUp(self) -> None:
        self.activities = {}
        self.sess = SessionManager(self.activities)

    def activeUserCount(self, date: str) -> int:
        return self.sess.active_users_count(self.sess.get_days_activity(date))

    def seedLoginData(self, date: str, users: List[int]):
        for user in users:
            activity = self.sess.get_days_activity(date)
            activity.add(user)

    def test_daysActivity_byLoginOneUser_getsOneActiveUser(self):
        today = get_date_str()
        self.seedLoginData(today, [1])
        self.assertEqual(1, self.activeUserCount(today))

    def test_daysActivity_pastDateWithoutPastHistory_getsZeroActiveUser(self):
        today, yesterday = get_date_str(), get_date_str(datetime.utcnow() - timedelta(days=1))
        self.seedLoginData(today, list(range(1000)))
        self.assertEqual(0, self.activeUserCount(yesterday))

    def test_inactiveUsersForAWeek_withSomeUsersLoginIn_getPositiveInactiveUserCount(self):
        total_users = 1500
        for d in range(0, 7):
            date = get_date_str(datetime.utcnow() - timedelta(days=d))
            users = list(range(d * 10, (d+1) * 10))
            self.seedLoginData(date, users)
        self.assertEqual(total_users - 70, self.sess.get_inactive_users_count_for_a_week(total_users))
