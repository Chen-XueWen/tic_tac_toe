#!/usr/bin/env python3
"""Simple command-line Tic Tac Toe game for two human players."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple


BOARD_SIZE = 5
TOTAL_CELLS = BOARD_SIZE * BOARD_SIZE


def generate_winning_lines(size: int) -> Tuple[Tuple[int, ...], ...]:
    """Produce all row, column, and diagonal winning lines for an N x N board."""
    lines = []

    # Rows
    for row in range(size):
        lines.append(tuple(row * size + col for col in range(size)))

    # Columns
    for col in range(size):
        lines.append(tuple(col + row * size for row in range(size)))

    # Main diagonals
    lines.append(tuple(i * size + i for i in range(size)))
    lines.append(tuple(i * size + (size - 1 - i) for i in range(size)))

    return tuple(lines)


WINNING_LINES: Tuple[Tuple[int, ...], ...] = generate_winning_lines(BOARD_SIZE)


@dataclass(frozen=True)
class GameState:
    """Represents the current board and active player."""

    board: Tuple[str, ...]
    active: str


def render_board(cells: Iterable[str]) -> str:
    """Return a human-friendly board representation."""
    cells = list(cells)
    cell_width = max(1, len(str(TOTAL_CELLS)))
    cell_fmt = f"{{:^{cell_width}}}"

    def display_value(idx: int) -> str:
        symbol = cells[idx]
        value = symbol if symbol != " " else str(idx + 1)
        return cell_fmt.format(value)

    rows = []
    for start in range(0, TOTAL_CELLS, BOARD_SIZE):
        row = " | ".join(display_value(i) for i in range(start, start + BOARD_SIZE))
        rows.append(f" {row} ")
    divider = "\n" + "+".join("-" * (cell_width + 2) for _ in range(BOARD_SIZE)) + "\n"
    return divider.join(rows)


def check_winner(board: Iterable[str]) -> Optional[str]:
    """Return the winning symbol if there is one."""
    cells = list(board)
    for line in WINNING_LINES:
        first = cells[line[0]]
        if first != " " and all(cells[idx] == first for idx in line[1:]):
            return first
    return None


def is_draw(board: Iterable[str]) -> bool:
    """Return True if the board is completely filled."""
    return all(cell != " " for cell in board)


def get_move(player: str, board: List[str]) -> int:
    """Prompt the active player for a move and return the chosen slot index."""
    while True:
        raw = input(f"Player {player}, choose a position (1-{TOTAL_CELLS}): ").strip()
        if not raw.isdigit():
            print(f"Please enter a number between 1 and {TOTAL_CELLS}.")
            continue
        slot = int(raw) - 1
        if slot not in range(TOTAL_CELLS):
            print("That position is outside the board. Try again.")
            continue
        if board[slot] != " ":
            print("That square is already taken. Choose another.")
            continue
        return slot


def make_move(state: GameState, slot: int) -> GameState:
    """Place the active player's mark on the board and switch the turn."""
    board = list(state.board)
    board[slot] = state.active
    next_player = "O" if state.active == "X" else "X"
    return GameState(tuple(board), next_player)


def new_game(starting_player: str = "X") -> GameState:
    """Return a fresh game state."""
    return GameState(board=(" ",) * TOTAL_CELLS, active=starting_player)


def evaluate_state(state: GameState) -> Optional[str]:
    """Return 'X' or 'O' for winner, 'draw' for stalemate, or None to continue."""
    winner = check_winner(state.board)
    if winner:
        return winner
    if is_draw(state.board):
        return "draw"
    return None


def play_round() -> None:
    """Run a single game of Tic Tac Toe."""
    state = new_game()

    while True:
        print("\n" + render_board(state.board))
        slot = get_move(state.active, list(state.board))
        state = make_move(state, slot)

        outcome = evaluate_state(state)
        if outcome in ("X", "O"):
            print("\n" + render_board(state.board))
            print(f"\nPlayer {outcome} wins!")
            return

        if outcome == "draw":
            print("\n" + render_board(state.board))
            print("\nIt's a draw!")
            return


def want_to_continue() -> bool:
    """Ask the players if they want another round."""
    while True:
        answer = input("Play again? [y/n]: ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


def main() -> None:
    print("Welcome to Tic Tac Toe!")
    try:
        while True:
            play_round()
            if not want_to_continue():
                print("Thanks for playing!")
                break
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")


if __name__ == "__main__":
    main()
