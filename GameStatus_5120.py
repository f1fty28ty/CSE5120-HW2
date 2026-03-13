# -*- coding: utf-8 -*-

import numpy as np

"""
GameStatus_5120.py

This file defines the `GameStatus` class, which represents the current board and turn.
It is used by:
- The GUI (to apply moves and detect game-over)
- The search agents (minimax/negamax) to evaluate states and generate legal moves

Board encoding:
- 0  : empty
- 1  : X
- -1 : O

Turn encoding (matches `get_new_state`):
- If `turn_O` is True  -> the next move written is X (1)
- If `turn_O` is False -> the next move written is O (-1)
"""

class GameStatus:


    def __init__(self, board_state, turn_O, win_length=3):
        """
        Create a new game state snapshot.

        Args:
            board_state: NumPy 2D array containing values in {0, 1, -1}.
            turn_O: Boolean that determines what value will be placed next:
                - True  -> place X (1)
                - False -> place O (-1)
            win_length: Number of consecutive marks needed to win.
                        Defaults to 3; use 4 for 4x4 boards, 5 for 5x5 boards.
        """

        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0
        self.win_length = win_length

        self.winner = ""
    """
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """

    def is_terminal(self):
        """
        Check if the state is terminal (game over) and set `self.winner`.

        Current behavior:
- The game ends immediately if a win_length-in-a-row exists for either player.
- Otherwise, the game ends in a draw when the board is full.

        Returns:
            True if the game has ended, otherwise False.
        """
        """
        For 3x3, normal tic-tac toe behavior is used.
        For larger boards, the game ends when the board is full 
        & the winner is decided by the cumulative triplet score
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])

        # Standard 3x3 behavior can be kept
        if rows == 3 and cols ==3:
            final_score = self.get_scores(True)

            if final_score > 0:
                self.winner = "X"
                return True
            elif final_score < 0:
                self.winner = "O"
                return True
            
            for r in range(rows):
                for c in range(cols):
                    if self.board_state[r][c] == 0:
                        return False
                    
            self.winner = "Draw"
            return True
        # For larger boards, logic is to keep playing until the board is full
        for r in range(rows):
            for c in range(cols):
                if self.board_state[r][c] == 0:
                    return False
        final_score = self.get_scores(True)

        if final_score > 0:
            self.winner = "X"
        elif final_score < 0:
            self.winner = "O"
        else:
            self.winner = "Draw"
        return True
        

    def get_scores(self, terminal):

        """
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
        """
        Compute an evaluation score for the current board.

        Scoring:
        - +1 for each X triplet found
        - -1 for each O triplet found

        For this HW, larger-board scoring is based on matching triplets measured cumulatively across the board.

        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        # Terminal check uses full win_length; heuristic uses win_length-1
        check_point = 3

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    segment = []
                    # Build a run of length `check_point` starting at (r, c) in direction (dr, dc).
                    for step in range(check_point):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < rows and 0 <= nc < cols:
                            segment.append(self.board_state[nr][nc])

                    if len(segment) == check_point:
                        # Count uniform segments only (all X or all O).
                        if all(v == 1 for v in segment):
                            scores += 1
                        elif all(v == -1 for v in segment):
                            scores -= 1

        return scores

    def get_negamax_scores(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
        """
        Compute a negamax evaluation score.

        follows the same triplet-based board logic as 'get_scores()',
        but uses a larger score magnitude for search.
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        # keep negamax aligned with the same triplet-based scoring rule
        check_point = 3

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    segment = []
                    # Same scan as `get_scores()`, but with a larger magnitude per segment.
                    for step in range(check_point):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < rows and 0 <= nc < cols:
                            segment.append(self.board_state[nr][nc])
                    if len(segment) == check_point:
                        if all(v == 1 for v in segment):
                            scores += 100
                        elif all(v == -1 for v in segment):
                            scores -= 100

        # Perspective adjustment: return a score aligned to the player-to-move.
        return scores * (-1 if self.turn_O else 1)

    def get_moves(self):
        moves = []
        """
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
        """
        Return a list of all legal moves (empty cells).

        Returns:
            List of (row, col) tuples.
        """
        num_rows = self.board_state.shape[0]
        num_cols = self.board_state.shape[1]
        for r in range(num_rows):
            for c in range(num_cols):
                if self.board_state[r][c] == 0:
                    moves.append((r, c))
        return moves


    def get_new_state(self, move):
        """
        Return a NEW GameStatus after applying the given move.

        This function does not mutate the current object. It copies the board, applies
        the next player's value, and flips `turn_O`. win_length is preserved.
        """
        new_board_state = self.board_state.copy()
        x, y = move[0], move[1]
        # Apply the current player's mark, then toggle to the other player.
        new_board_state[x, y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O, self.win_length)