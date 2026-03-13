from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
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
            if beta <= alpha:
                break

    # return value, best_move
    return value, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth==0) or (terminal):
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
        result, _ = negamax(next_state, depth - 1, -turn_multiplier, -beta, -alpha)
        result = -result
        if result > value:
            value = result
            best_move = candidate
        if result > alpha:
            alpha = result
        if alpha >= beta:
            break

    #return value, best_move
    return value, best_move
