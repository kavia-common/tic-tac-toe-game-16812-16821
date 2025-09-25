"""
Data models and schemas for the Tic Tac Toe backend.

This module defines the Pydantic models used by the API for request and response
payloads, along with internal domain models representing the game state.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class Player(str, Enum):
    """Enumeration for Tic Tac Toe players."""
    X = "X"
    O = "O"


class GameStatus(str, Enum):
    """Enumeration for overall game status."""
    IN_PROGRESS = "IN_PROGRESS"
    X_WON = "X_WON"
    O_WON = "O_WON"
    TIE = "TIE"


class GameState(BaseModel):
    """
    Immutable snapshot of the current game state.

    Attributes:
    - game_id: Unique identifier assigned to the game.
    - board: 3x3 board represented as a flat list of 9 elements ("X", "O", or None).
    - next_player: The player who should make the next move.
    - status: The current status of the game (in progress, won, tie).
    - winner: The player that won if applicable.
    - moves_count: Number of moves played so far.
    """
    model_config = ConfigDict(use_enum_values=True)

    game_id: str = Field(..., description="Unique game identifier")
    board: List[Optional[Player]] = Field(
        ..., min_length=9, max_length=9, description="Flat list of 9 items representing the board cells."
    )
    next_player: Optional[Player] = Field(
        None, description="Which player is to move next; None if game is finished."
    )
    status: GameStatus = Field(..., description="Current status of the game")
    winner: Optional[Player] = Field(None, description="Winner if any")
    moves_count: int = Field(..., ge=0, le=9, description="How many moves have been made")


# PUBLIC_INTERFACE
class NewGameRequest(BaseModel):
    """
    Request model to create a new game.

    Attributes:
    - first_player: Optional player to start; if omitted, defaults to 'X'.
    """
    first_player: Optional[Player] = Field(
        None, description="Player to start the game; defaults to X"
    )


# PUBLIC_INTERFACE
class NewGameResponse(GameState):
    """
    Response model after creating a new game. Inherits GameState.
    """
    pass


# PUBLIC_INTERFACE
class MoveRequest(BaseModel):
    """
    Request model for making a move.

    Attributes:
    - position: Index in the board (0..8)
    - player: The player attempting the move
    """
    position: int = Field(..., ge=0, le=8, description="Board index from 0 to 8")
    player: Player = Field(..., description="Player making the move")


# PUBLIC_INTERFACE
class ErrorResponse(BaseModel):
    """
    Error payload model standardized for API error responses.
    """
    detail: str = Field(..., description="Error detail message")
