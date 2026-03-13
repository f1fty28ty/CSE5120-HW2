# CSE5120 HW2 — Multi-Agent Tic Tac Toe (GUI)

This project implements a Tic Tac Toe variant with:
- A **pygame GUI** (`large_board_tic_tac_toe.py`)
- **Minimax** and **Negamax** with alpha–beta pruning (`multiAgents.py`)
- A game state model used by both GUI and agents (`GameStatus_5120.py`)

## Requirements
- Python 3
- `pygame`
- `numpy`

Install dependencies:

```bash
python3 -m pip install pygame numpy
```

## Run the game
From this folder:

```bash
cd "/Users/f1fty28ty/School/5120/HW2"
python3 large_board_tic_tac_toe.py
```

## How to play (GUI)
- **Click buttons** at the top to choose:
  - Algorithm: **Minimax** or **Negamax**
  - Mode: **Human vs AI** or **Human vs Human**
  - Board size: **3x3**, **4x4**, **5x5**
- **Click a board cell** to place a move.
- **Reset** (top-right) clears the board and unlocks settings.

### Settings lock + series score
- Once you make the first board move, **settings are locked** for that match.
- After the match ends, you can **click the board** to start a **new round** with the same settings.
- The GUI tracks a running **Series** counter: X wins, O wins, Draws.

## Rules / scoring
### Board encoding
- `0` = empty
- `1` = X
- `-1` = O

### Turn convention
The `GameStatus.turn_O` field name comes from the starter template, but in this codebase:
- `turn_O == True`  → the next move placed is **X** (`1`)
- `turn_O == False` → the next move placed is **O** (`-1`)

### Game end condition (current behavior)
The game ends immediately when a **3-in-a-row** exists for either player (see `GameStatus_5120.py:is_terminal()`).
If there is no winner and the board is full, it is a draw.

## File overview
- `large_board_tic_tac_toe.py`: pygame GUI, input handling, match flow, calls AI.
- `GameStatus_5120.py`: board representation, move generation, scoring, terminal checks.
- `multiAgents.py`: minimax + negamax (alpha–beta), returns `(score, move)`.
