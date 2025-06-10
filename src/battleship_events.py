import time

from sea_battle_event.board import Board
from sea_battle_event.config import GameConfig
from sea_battle_event.enums import EventName
from sea_battle_event.event_manager import EnentManager
from sea_battle_event.game_manager import GameManager
from sea_battle_event.player import SimpleAIPlayer

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
    config = GameConfig(10, 10, 42, [1, 1, 1, 1, 2, 2, 2, 3, 3, 4] * 1)
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
    print(game_manager.board)
    print("time", end - start)
    print("acc", hits / guesses)
    print("hits", hits)
    print("guesses", guesses)
    print("turns", turns)


if __name__ == "__main__":
    main()
