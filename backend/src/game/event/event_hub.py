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
        for o in self.observers.values():
            o.update(event)

    def subscribe(self, observer: EventObserver) -> bool:
        oid = id(observer)

        if oid in self.observers:
            return False

        self.observers[oid] = observer
        return True

    def unsusbscribe(self, observer: EventObserver) -> bool:
        oid = id(observer)

        if oid not in self.observers:
            return False

        del self.observers[oid]
        return True
