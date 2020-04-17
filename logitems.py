import random
import uuid
from collections import namedtuple
from faker import Faker


UserAction = namedtuple("Action", ["verbs", "objects", "levels"])
HTTPStatus = namedtuple("HTTPStatus", ["codes", "levels"])
LogItem = namedtuple("LogItem", ["level", "event", "fields"])


class CreateLogItem:
    def __init__(self):
        self.fake = Faker()

    def create_random_log_item(self):
        types = ["create_user_log", "create_access_log", "create_cpu_log"]
        return getattr(self, random.choice(types))()

    def create_user_log(self):
        user_objects = ["Account", "Profile", "Document", "Post", "Comment"]

        actions = [
            UserAction(
                verbs=["Created", "Updated", "Viewed"],
                objects=user_objects,
                levels=["info", "debug"],
            ),
            UserAction(
                verbs=["Permissions Changed", "Rejected"],
                objects=user_objects,
                levels=["warning"],
            ),
            UserAction(
                verbs=["Deleted", "Revoked"],
                objects=user_objects,
                levels=["critical", "error"],
            ),
        ]

        action_taken = random.choice(actions)

        return LogItem(
            level=random.choice(action_taken.levels),
            event=f"{random.choice(action_taken.objects)} {random.choice(action_taken.verbs)}",
            fields={
                "type": "user",
                "uuid": uuid.uuid4().hex,
                "username": self.fake.user_name(),
                "job_title": self.fake.job(),
                "email": self.fake.email(),
                "avatar": f"https://i.pravatar.cc/150?u={uuid.uuid4().hex}",
                "url": self.fake.url(),
                "ip": self.fake.ipv6(),
            },
        )

    def create_access_log(self):
        statuses = [
            HTTPStatus(codes=[200, 201, 304], levels=["info", "debug"]),
            HTTPStatus(
                codes=[204, 300, 301, 302, 307, 308, 401, 402, 403, 405],
                levels=["warning"],
            ),
            HTTPStatus(
                codes=[400, 404, 410, 429, 500, 501, 502, 503],
                levels=["critical", "error"],
            ),
        ]

        status = random.choice(statuses)
        url = self.fake.url()
        code = random.choice(status.codes)

        return LogItem(
            level=random.choice(status.levels),
            event=f"[{code}] - {url}",
            fields={
                "type": "access",
                "uuid": uuid.uuid4().hex,
                "status": code,
                "url": url,
                "path": self.fake.uri_path(),
                "ip": self.fake.ipv4_public(),
            },
        )

    def create_cpu_log(self):
        return LogItem(
            level="info",
            event=f"server load",
            fields={
                "type": "cpu",
                "uuid": uuid.uuid4().hex,
                "servers": {
                    "Camano": random.randint(0, 50),
                    "Rosario": random.randint(80, 100),
                    "Monaco": random.randint(30, 80),
                },
            },
        )
