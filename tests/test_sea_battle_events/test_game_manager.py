from sea_battle_event.board import Board
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager
from sea_battle_event.game_manager import GameManager
from sea_battle_event.player import SimpleAIPlayer


def test__init__():
    game_manager = GameManager(
        EnentManager(), GameConfig(10, 10, 42, [1, 2]), SimpleAIPlayer, Board
    )
    game_manager.init_game()
    game_manager.process_events()
    assert game_manager.board is not None
    assert game_manager.player is not None
    assert game_manager.running is True
    game_manager.new_turn()
    assert game_manager.event_manager.event_queue[-1] == (EventName.NEW_TURN, (), {})
    game_manager.game_over()
    assert game_manager.running is False
