# Reference - https://github.com/lfpelison/ine5430-gomoku/blob/master/src/minimax.py

def set_base_heuristic(board):
    base_heuristic = [[-999] * board.ncols for _ in range(board.nrows)]

    for row in range(board.nrows):
        for col in range(board.ncols):
            if board.board[row][col].is_valid_cell:
                base_heuristic[row][col] = 0

    return base_heuristic


def minimax(state, depth=2):
    """
        Minimax algorithm
    """


    def max_play(state, alpha, beta, d):
        if state.is_terminal() or d >= depth:
            return state.heuristic_value
        node_value = float('-inf')
        for i, move in enumerate(state.available_moves):
            node_value = max(node_value, min_play(state.next_state(move),
                                                  alpha, beta, d + 1))
            if node_value >= beta:
                # print('val:{} move:{}'.format(node_value, move)) # To debug
                return node_value
            alpha = max(alpha, node_value)
        # print('didnt pruned')
        return node_value


    def min_play(state, alpha, beta, d):
        if state.is_terminal() or d >= depth:
            return state.heuristic_value
        node_value = float('inf')
        for i, move in enumerate(state.available_moves):
            node_value = min(node_value, max_play(state.next_state(move),
                                                  alpha, beta, d + 1))
            if node_value <= alpha:
                # print('val:{} move:{}'.format(node_value, move)) # To debug
                return node_value
            beta = min(beta, node_value)
        # print('didnt pruned')
        return node_value


    alpha = float('-inf')
    beta = float('inf')
    node_value = float('-inf')
    next_move = state.available_moves[0]
    for i, move in enumerate(state.available_moves):
        neighbor_value = min_play(state.next_state(move), alpha, beta, 1)
        # print('child {}/{}: '.format(i, len(state.available_moves)))
        if neighbor_value > node_value:
            node_value = neighbor_value
            next_move = move
        alpha = max(alpha, node_value)
    return next_move
