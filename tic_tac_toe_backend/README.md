# Tic Tac Toe Backend (FastAPI)

This service implements a simple Tic Tac Toe backend with in‑memory game storage.

Endpoints:
- GET / — Health check
- POST /games — Create a new game (optional body: {"first_player": "X" | "O"})
- GET /games/{game_id} — Get current game state
- POST /games/{game_id}/moves — Submit a move (body: {"position": 0..8, "player": "X" | "O"})

Models:
- GameState: includes board (list of 9 items with "X"/"O"/null), next_player, status, winner, moves_count.
- MoveRequest: position and player.
- NewGameRequest: optional first_player.

Notes:
- Storage is in-memory and not shared across processes.
- For production, use a shared store like Redis and swap out store.py accordingly.

Run:
- uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
