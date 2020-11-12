"""
Centralised hub for events
"""

from abc import ABC, abstractmethod

from src.game.event.event import GameEvent


class EventObserver(ABC):
    @abstractmethod
    def update(self, event: GameEvent):
        pass


class EventHub:
    def __init__(self):
        self.observers = {}

    def publish(self, event: GameEvent):
        """Pushlishes event to observers

        Args:
            event (GameEvent): event to be published
        """
        for o in self.observers.values():
            o.update(event)

    def subscribe(self, observer: EventObserver) -> bool:
        """Subscribes to an event

        Args:
            observer (EventObserver): the subscribing observer

        Returns:
            bool: False if already subscribed
        """
        oid = id(observer)

        if oid in self.observers:
            return False

        self.observers[oid] = observer
        return True

    def unsusbscribe(self, observer: EventObserver) -> bool:
        """Unsubscribe from event

        Args:
            observer (EventObserver): the unsubscribing observer

        Returns:
            bool: False if not subscribed to begin with
        """
        oid = id(observer)

        if oid not in self.observers:
            return False

        del self.observers[oid]
        return True
