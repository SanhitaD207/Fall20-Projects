# Reference - https://github.com/lfpelison/ine5430-gomoku/blob/master/src/minimax.py


UTILITY = {
    'f': {
        'captured_e': 500,
        'captured_g': 250,
        'neutral': 100
    },
    'g_e': {
        'captured_f': 500,
        'partial_blocked_f': 250,
        'neutral': 100
    }
}


def calculate_heuristic(board, player, player_c_i, player_c_f, opp_c_i, opp_c_f):
    # TODO - Code to calculate heuristic value for player based on rules defined
    """
    Calculates the heuristic value at the end of the minimax execution
    :param board: Current Board State
    :param player: Either Fox 'f' or GeeseElephant 'g_e'
    :param player_c_i: Player Collection Initial
    :param player_c_f: Player Collection Final
    :param opp_c_i: Opponent Collection Initial
    :param opp_c_f: Opponent Collection Final
    :return value: numeric heuristic value
    """

    value = 0
    if player == 'f':
        if len(player_c_i.items()) > len(player_c_f.items()):
            value -= UTILITY['g_e']['captured_f']

        if len(opp_c_i.items()) > len(opp_c_f.items()):
            animals_captured = [x for x in opp_c_f if x not in opp_c_i]

            for animal in animals_captured:
                value += UTILITY['f'][f'captured_{animal[0]}']
        else:
            value += UTILITY['f']['neutral']

    else:
        if len(opp_c_i.items()) > len(opp_c_f.items()):
            value += UTILITY['g_e']['captured_f']

        if len(player_c_i.items()) > len(player_c_f.items()):
            animals_captured = [x for x in player_c_f if x not in player_c_i]

            for animal in animals_captured:
                value -= UTILITY['f'][f'captured_{animal[0]}']
        else:
            value += UTILITY['g_e']['neutral']

    return value


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
