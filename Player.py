from Helper import get_single_step_moves, get_hop_moves


class Player:
    def move(self, board, r, c, **kwargs):
        pass


class GeeseElephantPlayer(Player):
    def __init__(self):
        self.geese_collection = {}
        self.elephant_collection = {}


    def move(self, board, r, c, **kwargs):
        pass


    def get_goose_available_moves(self, board):
        # TODO - Single cell movement for goose
        # TODO - preference to move that leads to surrounding a fox
        moves = {}
        for key, val in self.geese_collection.items():
            moves[key] = get_single_step_moves(board, *val)
            print(f'\n{key} available moves: ', moves[key])

        return moves


    def get_elephant_available_moves(self, board):
        # TODO - Single cell movement for elephant
        # TODO - preference to move that leads to surrounding a fox
        moves = {}
        for key, val in self.elephant_collection.items():
            moves[key] = get_single_step_moves(board, *val)
            print(f'\n{key} available moves: ', moves[key])

        return moves


class FoxPlayer(Player):
    def __init__(self):
        self.fox_collection = {}


    def move(self, board, r, c, **kwargs):
        pass


    def get_fox_available_moves(self, board):
        # TODO - Preference to move that leads to killing goose
        # TODO - Single cell movement if no goose/elephant
        # TODO - Preference to move that leads to surrounding an elephant if close to other fox
        moves = {}
        for key, val in self.fox_collection.items():
            moves[key] = get_hop_moves(board, *val) + get_single_step_moves(board, *val)
            print(f'\n{key} available moves: ', moves[key])

        return moves
