from asyncio import Event

from fastapi import WebSocket
from src import crud
from src.core.async_exit import wait_until_exit

from .notif_event import GenericEvent, NotifEvent


class NotificationHub:
    """
    Cental location for notification events to be published. Allows for relay of
    notification events to the appropriate [Notifier] instances.
    """

    def __init__(self):
        self.notifiers = dict()

    def publish(self, event):
        """
        Publish a notification [event] to notifiers
        """
        uid = event.user.uid

        # record notification
        msg = event.to_msg()
        if msg.msg_type == "notif":
            crud.user.add_notification(msg=msg, user=event.user.model, db=event.user.db)

        # ping notifiers
        if uid not in self.notifiers:
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
    """
    Takes care of sending notifications to a particular client.
    If the same user is accessing the system through multiple clients/devices, then
    a notifier should be present for each of those clients.
    """

    def __init__(self, user):
        self.user = user
        self.events = []
        self.has_event = Event()

    def update(self, event: NotifEvent):
        """Publishes an event to the notifier

        Args:
            event (NotifEvent): the event to publish
        """
        self.events.append(event)
        self.has_event.set()

    async def flush(self, ws: WebSocket):
        """Sends all events to the client and clears the event backlog

        Args:
            ws (WebSocket): client websocket
        """
        await wait_until_exit(self.has_event.wait())

        for event in self.events:
            msg = event.to_msg().dict()
            await ws.send_json(dict(msg=msg, is_error=False, type=msg["msg_type"]))

        self.events = []
        self.has_event.clear()

    @property
    def uid(self):
        return self.user.uid


notif_hub = NotificationHub()
send_msg = lambda user, msg: notif_hub.publish(GenericEvent(user=user, msg=msg))
