# Battleship Game

A Python implementation of the classic Battleship game, demonstrating different architectural approaches. This project features:

* A command-line interface.
* Two distinct game logic implementations:
  * A direct, synchronous version.
  * An event-driven version showcasing a more decoupled architecture.
* A simple AI opponent.
* Configurable board sizes and ship fleets.
* Unit tests for core components and game logic.

## Project Structure

* `src/`: Contains the main source code.
  * `battleship.py`: Entry point for the direct (synchronous) version of the game.
  * `battleship_events.py`: Entry point for the event-driven version of the game.
  * `common/`: Core data structures like `Grid`, `Pos`, and `Ship` used by both game versions.
  * `sea_battle/`: Modules specific to the direct version of the game (Board, Player, Enums).
  * `sea_battle_event/`: Modules specific to the event-driven version (Board, Player, Config, EventManager, GameManager, Enums, Protocols).
* `tests/`: Contains unit tests for the project, organized to mirror the `src/` structure.

## Features

* **Classic Battleship Gameplay:** Place your ships and try to sink your opponent's fleet.
* **Two Game Modes:**
  * **Direct Mode (`battleship.py`):** A straightforward implementation where game components interact directly.
  * **Event-Driven Mode (`battleship_events.py`):** A more advanced implementation using an event manager to decouple game logic, making components more modular and reactive.
* **Simple AI:** Play against a basic AI that makes random valid guesses, with some logic to hunt for ships after a hit.
* **Configurable Games:**
  * The direct version (`battleship.py`) can be configured by modifying parameters directly in its `main()` function (e.g., board size, ship list).
  * The event-driven version (`battleship_events.py`) uses a `GameConfig` object for setup.
* **Tested Core Logic:** Includes a suite of `pytest` unit tests to ensure the reliability of game mechanics.

## How to Run

1. **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd battleship
    ```

2. **Set up a virtual environment (recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install .
    ```

    If you also want to run tests or use development tools:

    ```bash
    pip install ".[test,dev]"
    ```

4. **Run the game:**
    * **Direct Version:**

        ```bash
        python src/battleship.py
        ```

    * **Event-Driven Version:**

        ```bash
        python src/battleship_events.py
        ```

    *(Note: Both versions currently print game state and results to the console. The direct version simulates a large game by default for performance observation, while the event-driven version runs a smaller, standard game.)*

## Running Tests

To run the unit tests:

```bash
pytest
```

To include coverage reporting (ensure `pytest-cov` is installed):

```bash
pytest --cov=src
```

## Key Learnings & Concepts Demonstrated

* Object-Oriented Programming (OOP) in Python.
* Implementation of core game logic for Battleship.
* Comparison of direct vs. event-driven software architectures.
* Basic AI development for game opponents.
* Unit testing with `pytest`.
* Project setup with `pyproject.toml` and dependency management.
* Use of Python data classes and enums for clarity and structure.
