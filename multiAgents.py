"""
multiAgents.py

This file contains the adversarial search algorithms used by the GUI:
- `minimax` with alpha-beta pruning
- `negamax` with alpha-beta pruning

Both functions return:
    (best_score, best_move)

Where:
- `best_score` is the evaluation of the best move found.
- `best_move` is a (row, col) tuple usable by `GameStatus.get_new_state(move)`.
"""

from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    """
    Minimax search with alpha-beta pruning.

    Args:
        game_state: Current `GameStatus`.
        depth: Remaining search depth.
        maximizingPlayer: True for max node, False for min node.
        alpha: Best value achievable by max along the current path.
        beta: Best value achievable by min along the current path.

    Returns:
        (value, best_move)
    """
    terminal = game_state.is_terminal()
    if (depth == 0) or terminal:
        # Leaf node: evaluate board and stop searching.
        newScores = game_state.get_scores(terminal)
        return newScores, None

    """
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """
    best_move = None
    available_moves = game_state.get_moves()

    if maximizingPlayer:
        value = float('-inf')
        for candidate in available_moves:
            child_state = game_state.get_new_state(candidate)
            child_val, _ = minimax(child_state, depth - 1, False, alpha, beta)
            if child_val > value:
                value = child_val
                best_move = candidate
            if value > alpha:
                alpha = value
            # Alpha-beta cutoff: opponent already has a better option earlier in the tree.
            if beta <= alpha:
                break
    else:
        value = float('inf')
        for candidate in available_moves:
            child_state = game_state.get_new_state(candidate)
            child_val, _ = minimax(child_state, depth - 1, True, alpha, beta)
            if child_val < value:
                value = child_val
                best_move = candidate
            if value < beta:
                beta = value
            # Alpha-beta cutoff.
            if beta <= alpha:
                break

    # return value, best_move
    return value, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    """
    Negamax search with alpha-beta pruning.

    Negamax is a minimax variant that uses sign-flipping during recursion rather than
    alternating max/min logic explicitly.

    Notes for this homework:
    - The base evaluation is produced by `GameStatus.get_negamax_scores()`.
    - `turn_multiplier` is kept in the signature to match the template / recursion pattern.

    Returns:
        (value, best_move)
    """
    terminal = game_status.is_terminal()
    if (depth == 0) or terminal:
        # Leaf node: negamax evaluation is handled by GameStatus.get_negamax_scores().
        scores = game_status.get_negamax_scores(terminal)
        return scores, None

    """
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    
    """
    best_move = None
    value = float('-inf')
    all_moves = game_status.get_moves()

    for candidate in all_moves:
        next_state = game_status.get_new_state(candidate)
        # Negamax recursion: flip perspective and swap alpha/beta bounds.
        result, _ = negamax(next_state, depth - 1, -turn_multiplier, -beta, -alpha)
        result = -result
        if result > value:
            value = result
            best_move = candidate
        if result > alpha:
            alpha = result
        # Alpha-beta cutoff.
        if alpha >= beta:
            break

    #return value, best_move
    return value, best_move
