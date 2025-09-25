"""
Game engine for Tic Tac Toe.

This module contains the pure logic for Tic Tac Toe:
- Board representation and validation
- Turn tracking
- Move application
- Win/Tie detection

The engine is separated from transport concerns so it can be reused or tested independently.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from .models import Player, GameStatus, GameState


WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    # Rows
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # Cols
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # Diagonals
    (0, 4, 8),
    (2, 4, 6),
)


def _detect_winner(board: List[Optional[Player]]) -> Optional[Player]:
    """
    Returns the winner (Player.X or Player.O) if found, else None.
    """
    for a, b, c in WIN_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def _is_board_full(board: List[Optional[Player]]) -> bool:
    """True if no empty squares remain."""
    return all(cell is not None for cell in board)


# PUBLIC_INTERFACE
def new_game_state(game_id: str, first_player: Player = Player.X) -> GameState:
    """
    Create a new game state.

    Args:
        game_id: Unique identifier for the game.
        first_player: Which player moves first (defaults to Player.X).

    Returns:
        GameState: Initial game state snapshot.
    """
    board: List[Optional[Player]] = [None] * 9
    return GameState(
        game_id=game_id,
        board=board,
        next_player=first_player,
        status=GameStatus.IN_PROGRESS,
        winner=None,
        moves_count=0,
    )


# PUBLIC_INTERFACE
def apply_move(state: GameState, position: int, player: Player) -> GameState:
    """
    Apply a move to the given state and return a new updated state.

    Validation rules:
    - Game must be in progress.
    - Position must be in range and empty.
    - It must be the player's turn.

    After applying:
    - Check for winner.
    - If winner, set status and winner; next_player becomes None.
    - If tie, set status TIE; next_player becomes None.
    - Else, toggle next player.

    Args:
        state: Current game state.
        position: Index (0..8).
        player: Player making the move.

    Returns:
        A new GameState reflecting the move.
    """
    if state.status != GameStatus.IN_PROGRESS:
        raise ValueError("Game is already finished.")

    if state.next_player != player:
        raise ValueError("It is not the specified player's turn.")

    if position < 0 or position > 8:
        raise ValueError("Position out of range, must be 0..8.")

    if state.board[position] is not None:
        raise ValueError("Cell already occupied.")

    # Copy board and apply move
    new_board = list(state.board)
    new_board[position] = player
    new_moves = state.moves_count + 1

    winner = _detect_winner(new_board)
    if winner is not None:
        return GameState(
            game_id=state.game_id,
            board=new_board,
            next_player=None,
            status=GameStatus.X_WON if winner == Player.X else GameStatus.O_WON,
            winner=winner,
            moves_count=new_moves,
        )

    if _is_board_full(new_board):
        return GameState(
            game_id=state.game_id,
            board=new_board,
            next_player=None,
            status=GameStatus.TIE,
            winner=None,
            moves_count=new_moves,
        )

    next_player = Player.O if player == Player.X else Player.X
    return GameState(
        game_id=state.game_id,
        board=new_board,
        next_player=next_player,
        status=GameStatus.IN_PROGRESS,
        winner=None,
        moves_count=new_moves,
    )
