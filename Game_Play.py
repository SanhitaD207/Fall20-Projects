from Helper import print_board_is_valid, print_board_cell_value
from Player import GeeseElephantPlayer, FoxPlayer
from Board import Board


class Game_Play():

    def __init__(self):
        self.g_e_player = GeeseElephantPlayer()
        self.f_player = FoxPlayer()
        self.board = Board(self.f_player.fox_collection, self.g_e_player.geese_collection, self.g_e_player.elephant_collection)
        self.winning_player = None

    def is_game_over(self):
        if not self.f_player.fox_collection:
            self.winning_player = "2"
            return True

        if not self.g_e_player.geese_collection and not self.g_e_player.elephant_collection:
            self.winning_player = "1"
            return True

        if len(self.g_e_player.elephant_collection) < 2 and not self.g_e_player.geese_collection:
            self.winning_player = "1"
            return True

        if len(self.g_e_player.geese_collection) < 4 and not self.g_e_player.elephant_collection:
            self.winning_player = "1"
            return True

        return False

    def play_game(self):
        """

        """

        # Reference  - TictacToe Game from Assignment 4

        while not self.is_game_over():
            self.f_player.move(self.board)
            if not self.is_game_over():
                self.g_e_player.move(self.board)


game = Game_Play()
game.play_game()
