import time

from utils.timer import TimerManager

TimerManager.decorator_timers_enabled = False


from sea_battle_event.board import Board
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager
from sea_battle_event.game_manager import GameManager
from sea_battle_event.player import SimpleAIPlayer
from utils.fprint import fprint

# while game_running:
#     current_time = get_time()
#     delta_time = current_time - last_time

#     process_events()           // Handle all queued events
#     update(delta_time)        // Update game state
#     render()                  // Draw current state

#     cap_frame_rate()         // Maintain steady frame rate
#     last_time = current_time


def main():
    start = time.perf_counter()
    config = GameConfig(100, 100, 42, [1, 1, 1, 1, 2, 2, 2, 3, 3, 4] * 100)
    game_manager = GameManager(EnentManager(), config, SimpleAIPlayer, Board)
    game_manager.init_game()
    # last_time = 0

    while game_manager.running:
        game_manager.new_turn()

        # current_time = time.perf_counter()
        # delta_time = current_time - last_time
        # print(delta_time)

        game_manager.process_events()

        # last_time = current_time
    end = time.perf_counter()
    turns = 0
    guesses = 0
    hits = 0
    for entry in game_manager.event_manager.history:
        if entry[0] == EventName.PLAYER_GUESS:
            guesses += 1
        elif entry[0] == EventName.SHIP_HIT or entry[0] == EventName.SHIP_DESTROYED:
            hits += 1
        elif entry[0] == EventName.NEW_TURN:
            turns += 1
    # print(game_manager.board)
    fprint("time", end - start)
    fprint("acc", hits / guesses)
    fprint(hits=hits)
    fprint(guesses=guesses)
    fprint(turns=turns)
    TimerManager.print_all_decorator_timers(sort="avg_percent")


if __name__ == "__main__":
    main()
