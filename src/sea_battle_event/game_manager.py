from typing import Any

from sea_battle_event.board import Board
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager
from sea_battle_event.protocols import Player


class GameManager:
    def __init__(
        self,
        event_manager: EnentManager,
        config: GameConfig,
        player_class: type[Player],
        board_class: type[Board],
    ) -> None:
        self.event_manager = event_manager
        self.config = config

        self.player_class = player_class
        self.player = None
        self.board_class = board_class
        self.board = None

        self.running = False

        self.subscriptions()

    def subscriptions(self) -> None:
        self.event_manager.subscribe(EventName.GAME_OVER, self.game_over)
        self.event_manager.subscribe(EventName.SET_PLAYER, self.create_player)
        self.event_manager.subscribe(EventName.SET_BOARD, self.create_board)

    def init_game(self) -> None:
        self.event_manager.add_to_event_queue(EventName.GAME_INIT)
        self.event_manager.add_to_event_queue(EventName.SET_PLAYER, self.config)
        self.event_manager.add_to_event_queue(EventName.SET_BOARD, self.config)

        self.running = True

    def create_player(self, *_: Any) -> None:
        self.player = self.player_class(self.event_manager, self.config)

    def create_board(self, *_: Any) -> None:
        self.board = self.board_class(self.event_manager, self.config)

    def new_turn(self) -> None:
        self.event_manager.add_to_event_queue(EventName.NEW_TURN)

    def process_events(self) -> None:
        self.event_manager.process_events()

    def game_over(self, *_: Any) -> None:
        self.running = False
        print("Game Over")
