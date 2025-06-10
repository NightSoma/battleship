from collections import deque
from collections.abc import Callable
from typing import Any

from sea_battle_event.enums import EventName


class EnentManager:
    def __init__(self):
        self.subscribers: dict[EventName, list[Callable[[Any | None], Any | None]]] = {}
        self.event_queue: deque[tuple[EventName, tuple[Any, ...], dict[str, Any]]] = (
            deque()
        )
        self.history: list[tuple[EventName, tuple[Any, ...], dict[str, Any]]] = []

    def subscribe(self, event_name: EventName, subscriber: Callable[[Any], Any]):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(subscriber)

    def unsubscribe(self, event_name: EventName, subscriber: Callable[[Any], Any]):
        if event_name in self.subscribers:
            self.subscribers[event_name].remove(subscriber)

    def add_to_event_queue(self, event_name: EventName, *args: Any, **kwargs: Any):
        self.history.append((event_name, args, kwargs))
        self.event_queue.append((event_name, args, kwargs))

    def process_events(self):
        while self.event_queue:
            event_name, args, kwargs = self.event_queue.popleft()
            if event_name in self.subscribers:
                for callback in self.subscribers[event_name]:
                    callback(*args, **kwargs)
