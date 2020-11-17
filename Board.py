import numpy as np


class BoardCell:

    def __init__(self, cell_value=None):
        self.cell_value = cell_value
        self.is_valid_cell = True

    def reset_is_valid(self):
        self.is_valid_cell = False


class Board:

    def __init__(self):
        self.nrows = 7
        self.ncols = 7

        self.board = [[BoardCell() for _col in range(self.ncols)] for _row in range(self.nrows)]

    def set_invalid_points_on_board(self):

        for i in range(self.nrows):
            for j in range(self.ncols):
                if (i < 2 or i > 4) and (j < 2 or j > 4):
                    self.board[i][j].is_valid_cell = False
                else:
                    self.board[i][j].is_valid_cell = True

        self.print_board_is_valid()

    def print_board_is_valid(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                print(self.board[i][j].is_valid_cell, end=" ")
            print("")


board = Board()
board.set_invalid_points_on_board()
