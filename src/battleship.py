import time

from sea_battle.board import Board
from sea_battle.enums import HitResult
from sea_battle.player import SimplePlayer


def main():
    start = time.perf_counter()
    board = Board(100, 100, seed=42)
    board.fill_with_ships([1, 1, 1, 1, 2, 2, 2, 3, 3, 4] * 100)

    player = SimplePlayer(100, 100, seed=42)
    turns = 0
    guesses = 0
    hits = 0

    while board.num_ships_alive > 0:
        turns += 1
        guess_result: HitResult = HitResult.game_started
        while guess_result in [
            HitResult.game_started,
            HitResult.ship_hit,
            HitResult.ship_destroyed,
        ]:
            pos = player.get_guess()
            guesses += 1
            guess_result = board.check_hit(pos)

            if guess_result in [HitResult.ship_hit, HitResult.ship_destroyed]:
                hits += 1

            player.give_feedback(guess_result)

            if board.num_ships_alive <= 0:
                break
    end = time.perf_counter()
    print(board)
    print("time", end - start)
    print("acc", hits / guesses)
    print("hits", hits)
    print("guesses", guesses)
    print("turns", turns)

    pass


if __name__ == "__main__":
    main()
