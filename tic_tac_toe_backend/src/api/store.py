"""
In-memory store for Tic Tac Toe games.

This simple repository keeps game states by ID. For production or multi-instance
deployments, replace with a persistent/shared store (e.g., Redis or a database).
"""

from __future__ import annotations

import secrets
from typing import Dict, Optional

from .models import GameState
from .engine import new_game_state


class GameStore:
    """A minimal in-memory repository for game states."""

    def __init__(self) -> None:
        self._games: Dict[str, GameState] = {}

    # PUBLIC_INTERFACE
    def create_game(self, first_player=None) -> GameState:
        """
        Create a new game with a generated ID.

        Args:
            first_player: Optional Player to start first.

        Returns:
            GameState: Initial game state stored and returned.
        """
        game_id = self._generate_id()
        state = new_game_state(game_id, first_player=first_player) if first_player else new_game_state(game_id)
        self._games[game_id] = state
        return state

    # PUBLIC_INTERFACE
    def get_game(self, game_id: str) -> Optional[GameState]:
        """Retrieve a game state by ID."""
        return self._games.get(game_id)

    # PUBLIC_INTERFACE
    def save_game(self, state: GameState) -> None:
        """Persist the given state in the store."""
        self._games[state.game_id] = state

    # PUBLIC_INTERFACE
    def delete_game(self, game_id: str) -> None:
        """Delete a game by ID, if it exists."""
        self._games.pop(game_id, None)

    def _generate_id(self) -> str:
        """Generate a short, URL-safe unique ID."""
        return secrets.token_urlsafe(8)


# Singleton store for app usage.
store = GameStore()
