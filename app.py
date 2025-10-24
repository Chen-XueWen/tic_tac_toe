#!/usr/bin/env python3
"""Flask front-end for the Tic Tac Toe game."""

from __future__ import annotations

from typing import List

from flask import Flask, flash, redirect, render_template, request, session, url_for

from tic_tac_toe import (
    BOARD_SIZE,
    TOTAL_CELLS,
    GameState,
    evaluate_state,
    make_move,
    new_game,
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"  # Replace with a secure key for production.


def _set_state(state: GameState) -> None:
    session["board"] = list(state.board)
    session["active"] = state.active


def _get_state() -> GameState:
    board = session.get("board")
    active = session.get("active", "X")
    if not board or len(board) != TOTAL_CELLS:
        state = new_game()
        _set_state(state)
        return state
    return GameState(tuple(board), active)


def _board_rows(cells: List[str]) -> List[List[tuple[int, str]]]:
    rows: List[List[tuple[int, str]]] = []
    for start in range(0, TOTAL_CELLS, BOARD_SIZE):
        row = [(idx, cells[idx]) for idx in range(start, start + BOARD_SIZE)]
        rows.append(row)
    return rows


@app.route("/", methods=["GET"])
def index():
    state = _get_state()
    outcome = evaluate_state(state)
    cells = list(state.board)
    rows = _board_rows(cells)
    return render_template(
        "index.html",
        rows=rows,
        board_size=BOARD_SIZE,
        active_player=state.active,
        outcome=outcome,
        total_cells=TOTAL_CELLS,
    )


@app.post("/move")
def move():
    state = _get_state()
    outcome = evaluate_state(state)
    if outcome:
        flash("The game is finished. Start a new game to continue.")
        return redirect(url_for("index"))

    raw_position = request.form.get("position", "")
    try:
        position = int(raw_position)
    except ValueError:
        flash("Invalid move selection.")
        return redirect(url_for("index"))

    if position < 0 or position >= TOTAL_CELLS:
        flash("That position is outside the board.")
        return redirect(url_for("index"))

    if state.board[position] != " ":
        flash("That square is already taken.")
        return redirect(url_for("index"))

    updated_state = make_move(state, position)
    _set_state(updated_state)
    return redirect(url_for("index"))


@app.post("/reset")
def reset():
    _set_state(new_game())
    flash("Started a new game.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
