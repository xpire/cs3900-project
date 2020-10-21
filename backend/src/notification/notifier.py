from asyncio import Event, TimeoutError, wait_for
from collections import defaultdict
from typing import Iterable

from fastapi import WebSocket
from src.core.async_exit import wait_until_exit

from .notif_event import NotifEvent

# TODO make notifier work for multiple users
# class Notifier:
#     def __init__(self):
#         self.notifiers = defaultdict(PersonalNotifier)


class Notifier:
    def __init__(self):
        self.events = []
        self.has_event = Event()

    def publish(self, event: NotifEvent):
        self.events.append(event)
        self.has_event.set()

    # def publish_multi(self, events: Iterable[NotifEvent]):
    #     if events:
    #         self.events.extend(events)
    #         self.has_event.set()

    async def flush(self, ws: WebSocket):
        # TODO consider running these in parallel
        # but watching out for order-sensitive ones

        await wait_until_exit(self.has_event.wait())

        for event in self.events:
            print(dict(msg=event.dict(), is_error=False, type="notif"))
            await ws.send_json(dict(msg=event.dict(), is_error=False, type="notif"))

        self.events = []
        self.has_event.clear()


notifier = Notifier()
