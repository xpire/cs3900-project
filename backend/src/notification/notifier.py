from asyncio import Event, TimeoutError, wait_for

from fastapi import WebSocket
from src.core.async_exit import wait_until_exit
from src.core.utilities import log_msg

from .notif_event import NotifEvent


class NotificationHub:
    def __init__(self):
        self.notifiers = dict()

    def publish(self, event):
        """
        Publish a notification [event] to notifiers
        """
        uid = event.user.uid

        if uid not in self.notifiers:
            log_msg("Matching user to notify event is not found", "ERROR")
            return

        for notifier in self.notifiers[uid].values():
            notifier.update(event)

    def subscribe(self, notifier) -> bool:
        """
        Let [notifier] listen to future events
        """
        print("Subscribed a notifier")
        nid = id(notifier)
        uid = notifier.uid

        if uid not in self.notifiers:
            self.notifiers[uid] = {nid: notifier}
            return True

        elif nid in self.notifiers[uid]:
            return False

        else:
            self.notifiers[uid][nid] = notifier
            return True

    def unsusbscribe(self, notifier) -> bool:
        """
        Stop [notifier] from listening to future events
        """
        nid = id(notifier)
        uid = notifier.uid

        if uid not in self.notifiers or nid not in self.notifiers[uid]:
            return False

        del self.notifiers[uid][nid]

        if len(self.notifiers[uid]) == 0:
            del self.notifiers[uid]

        return True


class Notifier:
    def __init__(self, user):  # UserDM
        self.user = user
        self.events = []
        self.has_event = Event()

    def update(self, event: NotifEvent):
        self.events.append(event)
        self.has_event.set()

    async def flush(self, ws: WebSocket):
        await wait_until_exit(self.has_event.wait())

        for event in self.events:
            msg = event.dict()
            del msg["user"]

            await ws.send_json(dict(msg=msg, is_error=False, type="notif"))

        self.events = []
        self.has_event.clear()

    @property
    def uid(self):
        return self.user.uid


notif_hub = NotificationHub()