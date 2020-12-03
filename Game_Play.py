from copy import deepcopy
from random import choice

from Board import Board
from Helper import remove_dead_animal, remove_dead_foxes_and_elephants, print_board_cell_value, get_hop_moves
from Player import GeeseElephantPlayer, FoxPlayer


class GamePlay:

    def __init__(self):
        self.g_e_player = GeeseElephantPlayer()
        self.f_player = FoxPlayer()
        self.board = Board(self.f_player.fox_collection,
                           self.g_e_player.geese_collection,
                           self.g_e_player.elephant_collection)
        self.winning_player = None

        self.UTILITY = {
            'f': {
                'captured_e': 500,
                'captured_g': 250,
                'can_capture_e': 300,
                'can_capture_g': 200,
                'neutral': 50
            },
            'g_e': {
                'captured_f': 500,
                'partial_blocked_f': 250,
                'e_can_capture_f': 250,
                'neutral': 50
            }
        }


    @staticmethod
    def is_game_end_state(animal_collection):

        fox_collection = {k: v for k, v in animal_collection.items() if 'fox' in k}
        elephant_collection = {k: v for k, v in animal_collection.items() if 'ele' in k}
        geese_collection = {k: v for k, v in animal_collection.items() if 'ge' in k}

        if not fox_collection:
            return True

        elif not geese_collection and not elephant_collection:
            return True

        elif len(elephant_collection) < 2 and not geese_collection:
            return True

        elif len(geese_collection) < 4 and not elephant_collection:
            return True

        elif len(fox_collection) == 1 and len(elephant_collection) > 1:
            return True

        elif len(fox_collection) == len(elephant_collection) == len(geese_collection) == 1:
            return True

        return False


    def is_game_over(self):

        winning_player = ''
        if not self.f_player.fox_collection:
            winning_player = "GE"

        elif not self.g_e_player.geese_collection and not self.g_e_player.elephant_collection:
            winning_player = "F"

        elif len(self.g_e_player.elephant_collection) < 2 and not self.g_e_player.geese_collection:
            winning_player = "F"

        elif len(self.g_e_player.geese_collection) < 4 and not self.g_e_player.elephant_collection:
            winning_player = "F"

        elif len(self.f_player.fox_collection) == 1 and len(self.g_e_player.elephant_collection) > 1:
            winning_player = "GE"

        elif len(self.f_player.fox_collection) == len(self.g_e_player.elephant_collection) == len(
                self.g_e_player.geese_collection) == 1:
            winning_player = 'Draw'

        return winning_player


    def play_game(self, with_ai=False):
        """

        """

        # Reference  - TictacToe Game from Assignment 4

        if not with_ai:
            while not self.is_game_over():

                dead_goose_row, dead_goose_col = self.f_player.move(self.board)
                if dead_goose_row:
                    remove_dead_animal(self.board, dead_goose_row, dead_goose_col,
                                       self.g_e_player.geese_collection)
                remove_dead_foxes_and_elephants(self.board, self.f_player.fox_collection,
                                                self.g_e_player.elephant_collection)
                if not self.is_game_over():
                    self.g_e_player.move(self.board)
                    remove_dead_foxes_and_elephants(self.board, self.f_player.fox_collection,
                                                    self.g_e_player.elephant_collection)
            else:
                print('\n\nGame Winner is - {}'.format(self.is_game_over()))
        else:
            while not self.is_game_over():
                fox_piece, fox_move = self.minimax('f')
                dead_goose_row, dead_goose_col = self.f_player.move_ai(self.board, self.f_player.fox_collection,
                                                                       fox_piece, fox_move)
                if dead_goose_row:
                    remove_dead_animal(self.board, dead_goose_row, dead_goose_col,
                                       self.g_e_player.geese_collection)
                remove_dead_foxes_and_elephants(self.board, self.f_player.fox_collection,
                                                self.g_e_player.elephant_collection)
                print_board_cell_value(self.board.board)
                if not self.is_game_over():
                    ge_piece, ge_move = self.minimax('ge')

                    self.g_e_player.move_ai(self.board,
                                            self.g_e_player.geese_collection
                                            if 'ge' in ge_piece else self.g_e_player.elephant_collection,
                                            ge_piece, ge_move)

                    remove_dead_foxes_and_elephants(self.board, self.f_player.fox_collection,
                                                    self.g_e_player.elephant_collection)
                    print_board_cell_value(self.board.board)

                self.board.block_region(self.f_player.fox_collection, self.g_e_player.geese_collection,
                                        self.g_e_player.elephant_collection)

            else:
                print('\n\nGame Winner is - {}'.format(self.is_game_over()))


    @staticmethod
    def can_capture_goose(board, fox_collection):
        for value in fox_collection.values():
            row, col = value
            if get_hop_moves(board, row, col):
                return True

        return False


    @staticmethod
    def can_capture_elephant(board, fox_collection):
        nrows = board.nrows
        ncols = board.ncols
        for value in fox_collection.values():
            row, col = value
            adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

            for r, c in adjacent_coordinates:
                if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board.board[r][c].is_valid_cell:
                    continue
                if board.board[r][c].cell_value == 'E':
                    return True

        return False


    @staticmethod
    def can_e_capture_f(board, fox_collection):
        nrows = board.nrows
        ncols = board.ncols
        for value in fox_collection.values():
            row, col = value
            adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

            for r, c in adjacent_coordinates:
                if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board.board[r][c].is_valid_cell:
                    continue
                if board.board[r][c].cell_value == 'E':
                    return True

        return False


    @staticmethod
    def can_partially_block_fox(board, fox_collection):
        nrows = board.nrows
        ncols = board.ncols
        # count_blocked_sides = 0
        for value in fox_collection.values():
            count_blocked_sides = 0
            row, col = value
            adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

            for r, c in adjacent_coordinates:
                if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board.board[r][c].is_valid_cell:
                    count_blocked_sides += 1
                    continue
                if board.board[r][c].cell_value == 'E':
                    count_blocked_sides += 1
                    continue
                if not board.board[r][c].cell_value:
                    count_blocked_sides -= 1
                    continue

            count_hop_moves = len(get_hop_moves(board, row, col))
            count_blocked_sides = count_blocked_sides - 2 * count_hop_moves

            if count_blocked_sides >= 0:
                return True

        return False


    def calculate_heuristic(self, board, player, player_c_i, player_c_f, opp_c_i, opp_c_f):
        """
        Calculates the heuristic value at the end of the minimax execution
        :param player: Either Fox 'f' or GeeseElephant 'g_e'
        :param player_c_i: Player Collection Initial
        :param player_c_f: Player Collection Final
        :param opp_c_i: Opponent Collection Initial
        :param opp_c_f: Opponent Collection Final
        :return value: numeric heuristic value
        """

        value = 0
        # print('\nIn Heuristic Calculation\n')
        # print_board_cell_value(board.board)
        if player == 'f':
            if len(player_c_i.items()) > len(player_c_f.items()):
                value -= self.UTILITY['g_e']['captured_f']

            if self.can_capture_goose(board, player_c_f):
                value += self.UTILITY['f']['can_capture_g']

            if self.can_capture_elephant(board, player_c_f):
                value += self.UTILITY['f']['can_capture_e']

            if len(opp_c_i.items()) > len(opp_c_f.items()):
                animals_captured = [x for x in opp_c_i if x not in opp_c_f]

                for animal in animals_captured:
                    value += self.UTILITY['f'][f'captured_{animal[0]}']

        else:
            if len(opp_c_i.items()) > len(opp_c_f.items()):
                value -= self.UTILITY['g_e']['captured_f']

            if self.can_partially_block_fox(board, opp_c_f):
                value -= self.UTILITY['g_e']['partial_blocked_f']

            if self.can_e_capture_f(board, opp_c_f):
                value -= self.UTILITY['g_e']['e_can_capture_f']

            if len(player_c_i.items()) > len(player_c_f.items()):
                animals_captured = [x for x in player_c_i if x not in player_c_f]

                for animal in animals_captured:
                    value += self.UTILITY['f'][f'captured_{animal[0]}']

        if value == 0:
            value += 50

        return value * -1


    def max_play(self, initial_board, player, player_c_i, player_c_f, opp_c_i, opp_c_f, alpha, beta, d):

        if self.is_game_end_state({**player_c_f, **opp_c_f}) or d >= 2:
            return self.calculate_heuristic(initial_board, player, player_c_i, player_c_f, opp_c_i, opp_c_f)

        max_node_value = float('-inf')

        available_moves = self.fetch_minimax_internal_available_moves(player, initial_board, player_c_f)

        for board_piece, moves in available_moves.items():
            for move in moves:
                local_player_c_f = deepcopy(player_c_f)
                local_opp_c_f = deepcopy(opp_c_f)
                board = deepcopy(initial_board)
                if player == 'f':
                    dead_goose_row, dead_goose_col = self.f_player.move_ai(board, local_player_c_f, board_piece, move)
                    if dead_goose_row:
                        remove_dead_animal(board, dead_goose_row, dead_goose_col, local_opp_c_f)

                    elephant_collection = {k: v for k, v in local_opp_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, local_player_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in local_opp_c_f.items() if 'ge' in k}
                    local_opp_c_f = {**geese_collection, **elephant_collection}

                else:
                    self.g_e_player.move_ai(board, local_player_c_f, board_piece, move)

                    elephant_collection = {k: v for k, v in local_player_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, local_opp_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in local_player_c_f.items() if 'ge' in k}
                    local_player_c_f = {**geese_collection, **elephant_collection}

                max_node_value = max(max_node_value, self.min_play(board, 'ge' if player == 'f' else 'f',
                                                                   opp_c_i, local_opp_c_f,
                                                                   player_c_i, local_player_c_f,
                                                                   alpha, beta, d + 1))
                # if node_value >= beta:
                #     # print('val:{} move:{}'.format(node_value, move)) # To debug
                #     return node_value
                # alpha = max(alpha, node_value)
        # print('didnt pruned')
        return max_node_value


    def min_play(self, initial_board, player, player_c_i, player_c_f, opp_c_i, opp_c_f, alpha, beta, d):

        if self.is_game_end_state({**player_c_f, **opp_c_f}) or d >= 2:
            return self.calculate_heuristic(initial_board, player, player_c_i, player_c_f, opp_c_i, opp_c_f)

        min_node_value = float('inf')

        available_moves = self.fetch_minimax_internal_available_moves(player, initial_board, player_c_f)

        for board_piece, moves in available_moves.items():
            for move in moves:
                local_player_c_f = deepcopy(player_c_f)
                local_opp_c_f = deepcopy(opp_c_f)
                board = deepcopy(initial_board)
                if player == 'f':
                    dead_goose_row, dead_goose_col = self.f_player.move_ai(board, local_player_c_f, board_piece, move)
                    if dead_goose_row:
                        remove_dead_animal(board, dead_goose_row, dead_goose_col, local_opp_c_f)

                    elephant_collection = {k: v for k, v in local_opp_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, local_player_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in local_opp_c_f.items() if 'ge' in k}
                    local_opp_c_f = {**geese_collection, **elephant_collection}

                else:
                    self.g_e_player.move_ai(board, local_player_c_f, board_piece, move)

                    elephant_collection = {k: v for k, v in local_player_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, local_opp_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in local_player_c_f.items() if 'ge' in k}
                    local_player_c_f = {**geese_collection, **elephant_collection}

                min_node_value = min(min_node_value, self.max_play(board, 'ge' if player == 'f' else 'f',
                                                                   opp_c_i, local_opp_c_f,
                                                                   player_c_i, local_player_c_f,
                                                                   alpha, beta, d + 1))

                # if node_value <= alpha:
                #     # print('val:{} move:{}'.format(node_value, move)) # To debug
                #     return node_value
                # beta = min(beta, node_value)
        # print('didnt pruned')
        return min_node_value


    def minimax(self, player):
        """
        Executes the minimax algorithm to find best move.
        Reference - https://github.com/lfpelison/ine5430-gomoku/blob/master/src/minimax.py
        :param player:
        :return:
        """

        alpha = float('-inf')
        beta = float('inf')

        if player == 'ge':
            node_value = float('-inf')
        else:
            node_value = float('inf')

        initial_board = deepcopy(self.board)

        player_c_i, opp_c_i, available_moves = self.fetch_minimax_game_state(player, initial_board)

        next_move = []
        next_board_piece = []

        for board_piece, moves in available_moves.items():
            for move in moves:
                player_c_f = deepcopy(player_c_i)
                opp_c_f = deepcopy(opp_c_i)
                board = deepcopy(initial_board)
                if player == 'f':
                    dead_goose_row, dead_goose_col = self.f_player.move_ai(board, player_c_f, board_piece, move)
                    if dead_goose_row:
                        remove_dead_animal(board, dead_goose_row, dead_goose_col, opp_c_f)

                    elephant_collection = {k: v for k, v in opp_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, player_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in opp_c_f.items() if 'ge' in k}
                    opp_c_f = {**geese_collection, **elephant_collection}

                else:
                    self.g_e_player.move_ai(board, player_c_f, board_piece, move)

                    elephant_collection = {k: v for k, v in player_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, opp_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in player_c_f.items() if 'ge' in k}
                    player_c_f = {**geese_collection, **elephant_collection}

                neighbor_value = self.min_play(board, 'ge' if player == 'f' else 'f',
                                               opp_c_i, opp_c_f, player_c_i, player_c_f, alpha, beta, 1)
                # print('child {}/{}: '.format(i, len(state.available_moves)))
                # if (node_value == float('-inf') and neighbor_value > node_value) or \
                #         (abs(neighbor_value) > abs(node_value)):
                if (player == 'ge' and neighbor_value >= node_value) or \
                        (player == 'f' and neighbor_value <= node_value):
                    if neighbor_value == node_value:
                        next_board_piece.append(board_piece)
                        next_move.append(move)
                    else:
                        next_board_piece = [board_piece]
                        next_move = [move]

                    node_value = neighbor_value

                # alpha = max(alpha, node_value)
        idx = choice(range(len(next_board_piece)))
        return next_board_piece[idx], next_move[idx]


    def fetch_minimax_game_state(self, player, board):
        if player == 'f':
            player_c_i = deepcopy(self.f_player.fox_collection)
            opp_c_i = deepcopy({
                **self.g_e_player.geese_collection,
                **self.g_e_player.elephant_collection
            })
            available_moves = self.f_player.get_fox_available_moves(board, player_c_i, True)
        else:
            player_c_i = deepcopy({
                **self.g_e_player.geese_collection,
                **self.g_e_player.elephant_collection
            })
            opp_c_i = deepcopy(self.f_player.fox_collection)
            available_moves = {
                **self.g_e_player.get_goose_available_moves(
                    board, deepcopy(self.g_e_player.geese_collection), True),
                **self.g_e_player.get_elephant_available_moves(
                    board, deepcopy(self.g_e_player.elephant_collection), True)
            }

        return player_c_i, opp_c_i, available_moves


    def fetch_minimax_internal_available_moves(self, player, board, animal_collection):
        if player == 'f':
            available_moves = self.f_player.get_fox_available_moves(board, animal_collection, True)
        else:
            geese_collection = {k: v for k, v in animal_collection.items() if 'ge' in k}
            elephant_collection = {k: v for k, v in animal_collection.items() if 'ele' in k}

            available_moves = {
                **self.g_e_player.get_goose_available_moves(
                    board, geese_collection, True),
                **self.g_e_player.get_elephant_available_moves(
                    board, elephant_collection, True)
            }

        return available_moves


game = GamePlay()
game.play_game(True)
