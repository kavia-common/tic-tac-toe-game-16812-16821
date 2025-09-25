from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from .models import (
    NewGameRequest,
    NewGameResponse,
    MoveRequest,
    GameState,
    ErrorResponse,
    Player,
)
from .store import store
from .engine import apply_move

openapi_tags = [
    {"name": "Health", "description": "Service health and diagnostics"},
    {"name": "Games", "description": "Tic Tac Toe game management and moves"},
]

app = FastAPI(
    title="Tic Tac Toe API",
    description=(
        "A simple Tic Tac Toe backend service.\n\n"
        "Features:\n"
        "- Start a new game\n"
        "- Submit moves with validation\n"
        "- Retrieve current game state\n"
        "- Automatic win/tie detection"
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production restrict to known origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/", response_model=Dict[str, str], tags=["Health"], summary="Health Check", description="Check if the service is up.")
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON payload with a message confirming health.
    """
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.post(
    "/games",
    response_model=NewGameResponse,
    responses={400: {"model": ErrorResponse}},
    tags=["Games"],
    summary="Start a new game",
    description="Creates a new Tic Tac Toe game and returns its initial state.",
)
def create_game(payload: NewGameRequest | None = None) -> NewGameResponse:
    """
    Create a new game.

    Parameters:
        payload: Optional body specifying which player should start.

    Returns:
        The initial GameState, including a generated game_id.
    """
    first_player: Player | None = None
    if payload and payload.first_player:
        first_player = payload.first_player
    state = store.create_game(first_player=first_player)
    return NewGameResponse(**state.model_dump())


# PUBLIC_INTERFACE
@app.get(
    "/games/{game_id}",
    response_model=GameState,
    responses={404: {"model": ErrorResponse}},
    tags=["Games"],
    summary="Get game state",
    description="Returns the current state of a specific game by its ID.",
)
def get_game_state(
    game_id: str = Path(..., description="The unique ID of the game"),
) -> GameState:
    """
    Retrieve the current state of the game.

    Args:
        game_id: The game identifier.

    Returns:
        The current GameState.

    Raises:
        HTTPException 404 if not found.
    """
    state = store.get_game(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found.")
    return state


# PUBLIC_INTERFACE
@app.post(
    "/games/{game_id}/moves",
    response_model=GameState,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    tags=["Games"],
    summary="Submit a move",
    description=(
        "Submit a move to the game. Provide the position (0..8) and the player making the move. "
        "The server validates turn order, cell availability, and determines wins/ties."
    ),
)
def make_move(
    game_id: str = Path(..., description="The unique ID of the game"),
    payload: MoveRequest | None = None,
) -> GameState:
    """
    Apply a move to a game and return the updated state.

    Args:
        game_id: Game identifier.
        payload: MoveRequest containing position and player.

    Returns:
        Updated GameState.

    Raises:
        HTTPException 404 if game not found.
        HTTPException 400 for invalid input or illegal move.
    """
    state = store.get_game(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found.")

    if payload is None:
        raise HTTPException(status_code=400, detail="Move payload is required.")

    try:
        new_state = apply_move(state, position=payload.position, player=payload.player)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    store.save_game(new_state)
    return new_state
