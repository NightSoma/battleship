from typing import Protocol

from sea_battle_event.config import GameConfig
from sea_battle_event.event_manager import EnentManager


class Player(Protocol):
    def __init__(self, event_manager: EnentManager, config: GameConfig) -> None: ...
