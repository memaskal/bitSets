from locust import HttpUser, between, task
from src.TagsManager import TagsManager
import random


class WebsiteUser(HttpUser):
    wait_time = between(0, 1)
    counter = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cId = WebsiteUser.counter
        self.token = ""
        WebsiteUser.counter += 1

    def on_start(self):
        resp = self.client.post("/login", json={
            "username": "user_" + str(self.cId),
            "password": "user_" + str(self.cId)
        })
        self.token = resp.json().get("token", "")

    @task
    def updateUserTasks(self):
        """
        Select and update randomly 5 tags for the current user
        :return:
        """
        choices = 5
        self.client.post("/api/users/%d/tags?token=%s" % (self.cId, self.token), json={
            "tags": random.sample(TagsManager.TAG_KEYS, k=choices)
        })
