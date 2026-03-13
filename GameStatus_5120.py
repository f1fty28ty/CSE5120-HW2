# -*- coding: utf-8 -*-

import numpy as np
class GameStatus:


    def __init__(self, board_state, turn_O):

        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0

        self.winner = ""
    """
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """

    def is_terminal(self):
        final_score = self.get_scores(terminal=True)
        if final_score > 0:
            self.winner = "X"
            return True
        elif final_score < 0:
            self.winner = "O"
            return True

        empty_cells = 0
        for r in range(len(self.board_state)):
            for c in range(len(self.board_state[r])):
                if self.board_state[r][c] == 0:
                    empty_cells += 1
        if empty_cells == 0:
            self.winner = "Draw"
            return True
    
        return False

        
        

    def get_scores(self, terminal):

        """
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    segment = []
                    for step in range(3):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < rows and 0 <= nc < cols:
                            segment.append(self.board_state[nr][nc])
                    if len(segment) == 3:
                        if segment[0] == segment[1] == segment[2] == 1:
                            scores += 1
                        elif segment[0] == segment[1] == segment[2] == -1:
                            scores -= 1

        return scores

    def get_negamax_scores(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    segment = []
                    for step in range(3):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < rows and 0 <= nc < cols:
                            segment.append(self.board_state[nr][nc])
                    if len(segment) == 3:
                        if segment[0] == segment[1] == segment[2] == 1:
                            scores += 100
                        elif segment[0] == segment[1] == segment[2] == -1:
                            scores -= 100

        return scores * (-1 if self.turn_O else 1)

    def get_moves(self):
        moves = []
        """
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
        num_rows = self.board_state.shape[0]
        num_cols = self.board_state.shape[1]
        for r in range(num_rows):
            for c in range(num_cols):
                if self.board_state[r][c] == 0:
                    moves.append((r, c))
        return moves


    def get_new_state(self, move):
        new_board_state = self.board_state.copy()
        x, y = move[0], move[1]
        new_board_state[x,y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O)
