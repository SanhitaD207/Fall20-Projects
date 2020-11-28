from copy import deepcopy

from Board import Board
from Helper import remove_dead_animal, remove_dead_foxes_and_elephants
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
                'neutral': 100
            },
            'g_e': {
                'captured_f': 500,
                'partial_blocked_f': 250,
                'neutral': 100
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
                fox_move = self.minimax('f')
            else:
                print('\n\nGame Winner is - {}'.format(self.is_game_over()))


    def calculate_heuristic(self, player, player_c_i, player_c_f, opp_c_i, opp_c_f):
        # TODO - Code to calculate heuristic value for player based on rules defined
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
        if player == 'f':
            if len(player_c_i.items()) > len(player_c_f.items()):
                value -= self.UTILITY['g_e']['captured_f']

            if len(opp_c_i.items()) > len(opp_c_f.items()):
                animals_captured = [x for x in opp_c_f if x not in opp_c_i]

                for animal in animals_captured:
                    value += self.UTILITY['f'][f'captured_{animal[0]}']
            else:
                value += self.UTILITY['f']['neutral']

        else:
            if len(opp_c_i.items()) > len(opp_c_f.items()):
                value += self.UTILITY['g_e']['captured_f']

            if len(player_c_i.items()) > len(player_c_f.items()):
                animals_captured = [x for x in player_c_f if x not in player_c_i]

                for animal in animals_captured:
                    value -= self.UTILITY['f'][f'captured_{animal[0]}']
            else:
                value += self.UTILITY['g_e']['neutral']

        return value


    def max_play(self, board, player, player_c_i, player_c_f, opp_c_i, opp_c_f, alpha, beta, d):

        if self.is_game_end_state({**player_c_f, **opp_c_f}) or d >= 2:
            return self.calculate_heuristic(player, player_c_i, player_c_f, opp_c_i, opp_c_f)

        node_value = float('inf')

        board = deepcopy(board)

        player_c_i, opp_c_i, available_moves = self.fetch_minimax_game_state(player, board)

        for board_piece, moves in available_moves.items():
            for move in moves:
                player_c_f = deepcopy(player_c_i)
                opp_c_f = deepcopy(opp_c_i)
                if player == 'f':
                    dead_goose_row, dead_goose_col = self.f_player.move_ai(board, player_c_i, board_piece, move)
                    if dead_goose_row:
                        remove_dead_animal(board, dead_goose_row, dead_goose_col, opp_c_f)

                    elephant_collection = {k: v for k, v in opp_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, player_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in opp_c_f.items() if 'ge' in k}
                    opp_c_f = {**geese_collection, **elephant_collection}

                else:
                    self.g_e_player.move_ai(board, player_c_i, board_piece, move)

                    elephant_collection = {k: v for k, v in player_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, opp_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in player_c_f.items() if 'ge' in k}
                    player_c_f = {**geese_collection, **elephant_collection}

                node_value = max(node_value, self.min_play(board, 'ge' if player == 'f' else 'f',
                                                           player_c_i, player_c_f,
                                                           opp_c_i, opp_c_f,
                                                           alpha, beta, d + 1))
                if node_value >= beta:
                    # print('val:{} move:{}'.format(node_value, move)) # To debug
                    return node_value
                alpha = max(alpha, node_value)
        # print('didnt pruned')
        return node_value


    def min_play(self, board, player, player_c_i, player_c_f, opp_c_i, opp_c_f, alpha, beta, d):

        if self.is_game_end_state({**player_c_f, **opp_c_f}) or d >= 2:
            return self.calculate_heuristic(player, player_c_i, player_c_f, opp_c_i, opp_c_f)

        node_value = float('inf')

        board = deepcopy(board)

        player_c_i, opp_c_i, available_moves = self.fetch_minimax_game_state(player, board)

        for board_piece, moves in available_moves.items():
            for move in moves:
                player_c_f = deepcopy(player_c_i)
                opp_c_f = deepcopy(opp_c_i)
                if player == 'f':
                    dead_goose_row, dead_goose_col = self.f_player.move_ai(board, player_c_i, board_piece, move)
                    if dead_goose_row:
                        remove_dead_animal(board, dead_goose_row, dead_goose_col, opp_c_f)

                    elephant_collection = {k: v for k, v in opp_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, player_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in opp_c_f.items() if 'ge' in k}
                    opp_c_f = {**geese_collection, **elephant_collection}

                else:
                    self.g_e_player.move_ai(board, player_c_i, board_piece, move)

                    elephant_collection = {k: v for k, v in player_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, opp_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in player_c_f.items() if 'ge' in k}
                    player_c_f = {**geese_collection, **elephant_collection}

                node_value = min(node_value, self.max_play(board, 'ge' if player == 'f' else 'f',
                                                           player_c_i, player_c_f,
                                                           opp_c_i, opp_c_f,
                                                           alpha, beta, d + 1))
                if node_value <= alpha:
                    # print('val:{} move:{}'.format(node_value, move)) # To debug
                    return node_value
                beta = min(beta, node_value)
        # print('didnt pruned')
        return node_value


    def minimax(self, player, depth=2):
        """
        Executes the minimax algorithm to find best move.
        Reference - https://github.com/lfpelison/ine5430-gomoku/blob/master/src/minimax.py
        :param player:
        :param depth:
        :return:
        """

        alpha = float('-inf')
        beta = float('inf')
        node_value = float('-inf')

        board = deepcopy(self.board)

        player_c_i, opp_c_i, available_moves = self.fetch_minimax_game_state(player, board)

        board_piece, moves = list(available_moves.items())[0]
        next_move = (board_piece, moves[0])

        for board_piece, moves in available_moves.items():
            for move in moves:
                player_c_f = deepcopy(player_c_i)
                opp_c_f = deepcopy(opp_c_i)
                if player == 'f':
                    dead_goose_row, dead_goose_col = self.f_player.move_ai(board, player_c_i, board_piece, move)
                    if dead_goose_row:
                        remove_dead_animal(board, dead_goose_row, dead_goose_col, opp_c_f)

                    elephant_collection = {k: v for k, v in opp_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, player_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in opp_c_f.items() if 'ge' in k}
                    opp_c_f = {**geese_collection, **elephant_collection}

                else:
                    self.g_e_player.move_ai(board, player_c_i, board_piece, move)

                    elephant_collection = {k: v for k, v in player_c_f.items() if 'ele' in k}
                    remove_dead_foxes_and_elephants(board, opp_c_f, elephant_collection)

                    geese_collection = {k: v for k, v in player_c_f.items() if 'ge' in k}
                    player_c_f = {**geese_collection, **elephant_collection}

                neighbor_value = self.min_play(board, alpha, beta, 1)
                # print('child {}/{}: '.format(i, len(state.available_moves)))
                if neighbor_value > node_value:
                    node_value = neighbor_value
                    next_move = move
                alpha = max(alpha, node_value)
        return next_move


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


game = GamePlay()
game.play_game(True)
