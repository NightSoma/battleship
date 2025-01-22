from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager


class TestClass:
    def __init__(self):
        self.value = 0

    def func(self, value: int):
        self.value += value


def test_subscribe():
    event_manager = EnentManager()
    sub1, sub2 = TestClass(), TestClass()

    event_manager.subscribe(EventName.NEW_TURN, sub1.func)
    event_manager.subscribe(EventName.NEW_TURN, sub2.func)
    event_manager.add_to_event_queue(EventName.NEW_TURN, 1)

    assert event_manager.event_queue[0] == (EventName.NEW_TURN, (1,), {})
    assert event_manager.history[0] == (EventName.NEW_TURN, (1,), {})
    assert len(event_manager.subscribers[EventName.NEW_TURN]) == 2


def test_unsubscribe():
    event_manager = EnentManager()
    sub1, sub2 = TestClass(), TestClass()

    event_manager.subscribe(EventName.NEW_TURN, sub1.func)
    event_manager.subscribe(EventName.NEW_TURN, sub2.func)
    event_manager.unsubscribe(EventName.NEW_TURN, sub1.func)

    assert event_manager.subscribers[EventName.NEW_TURN] == [sub2.func]


def test_process_events():
    event_manager = EnentManager()
    sub1, sub2 = TestClass(), TestClass()

    event_manager.subscribe(EventName.NEW_TURN, sub1.func)
    event_manager.subscribe(EventName.NEW_TURN, sub2.func)
    event_manager.add_to_event_queue(EventName.NEW_TURN, 1)
    event_manager.unsubscribe(EventName.NEW_TURN, sub1.func)
    event_manager.process_events()

    assert sub1.value == 0
    assert sub2.value == 1
    assert len(event_manager.event_queue) == 0
