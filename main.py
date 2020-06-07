from tornado.web import Application, RequestHandler, url, authenticated, HTTPError
from tornado.ioloop import IOLoop
from src.TagsManager import TagsManager
from src.SessionManager import SessionManager
import json


class BaseHandler(RequestHandler):
    db = {}

    def get_current_user(self):
        token = self.get_query_argument("token")
        return self.db["users"].get(token)

    def authorized(self, user_id):
        if str(self.current_user["id"]) != user_id:
            # user tried to view another user's tags
            raise HTTPError(404, "Not found")


class LoginHandler(RequestHandler):
    def initialize(self, db, sesm: SessionManager) -> None:
        self.db = db
        self.sesm = sesm

    def search_user(self, username):
        for user in self.db["users"].values():
            if user["name"] == username:
                return user

    def post(self):
        """
        Implements dummy login, by sending username == password
        returns the user token with which the api calls are performed
        :return:
        """
        credentials = json.loads(self.request.body)
        username = credentials.get("username")
        password = credentials.get("password")
        if username and password and username == password:
            user = self.search_user(username)
            self.sesm.login(user["id"])
            return self.write({"username": username, "token": user["token"]})
        raise HTTPError(400)


class TagsHandler(BaseHandler):
    def initialize(self, db, tagsm: TagsManager) -> None:
        self.db = db
        self.tagsm = tagsm

    @authenticated
    async def get(self, user_id):
        self.authorized(user_id)
        self.write({"values": self.current_user["tags"]})

    @authenticated
    def post(self, user_id):
        self.authorized(user_id)
        tags = json.loads(self.request.body).get("tags")
        if tags:
            self.current_user["tags"] = tags
            self.tagsm.add_tags(self.current_user["id"], tags)


class StatsHandler(RequestHandler):
    def initialize(self, db, sesm: SessionManager, tagsm: TagsManager) -> None:
        self.db = db
        self.sesm = sesm
        self.tagsm = tagsm

    def get(self):
        total_users = len(self.db["users"])
        self.write({
            "offline_for_a_week": self.sesm.get_inactive_users_count_for_a_week(total_users),
            "users_with_tag1_and_tags2": self.tagsm.count_users_with_tags("tag1", "tag2"),
            "user_ids_with_tag1": list(self.tagsm.get_users_with_tag("tag1"))
        })


def create_users():
    users = {}
    for user_id in range(1000):
        token = "user_token_" + str(user_id)
        users[token] = {
            "id": user_id,
            "token": token,
            "name": "user_" + str(user_id),
            "tags": list()
        }
    return users


def create_tags():
    from pyroaring import BitMap
    tags = {tag: BitMap() for tag in TagsManager.TAG_KEYS}
    return tags


def create_user_history():
    return dict()


def make_app():
    db = {"users": create_users()}
    sesm = SessionManager(create_user_history())
    tagsm = TagsManager(create_tags())
    urls = [
        url("/login", LoginHandler, dict(db=db, sesm=sesm), name="login"),
        url(r"/api/users/([0-9]+)/tags", TagsHandler, dict(db=db, tagsm=tagsm), name="tags"),
        url("/stats", StatsHandler, dict(db=db, sesm=sesm, tagsm=tagsm), name="stats")
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3001)
    IOLoop.current().start()
