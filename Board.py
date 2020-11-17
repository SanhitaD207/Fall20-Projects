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

        self.set_invalid_points_on_board()

        self.fox_collection = {}
        self.geese_collection = {}
        self.elephant_collection = {}

        self.set_foxes_initial_position()
        self.set_elephant_initial_position()
        self.set_goose_initial_position()

    def set_foxes_initial_position(self):
        self.board[3][2].cell_value = 'F'
        self.fox_collection['fox_1'] = (3, 2)

        self.board[3][4].cell_value = 'F'
        self.fox_collection['fox_2'] = (3, 4)

        self.print_board_cell_value()
        print(self.fox_collection)

    def set_elephant_initial_position(self):
        self.board[4][0].cell_value = 'E'
        self.elephant_collection['ele_1'] = (4, 0)

        self.board[4][6].cell_value = 'E'
        self.elephant_collection['ele_2'] = (4, 6)

        self.board[6][3].cell_value = 'E'
        self.elephant_collection['ele_2'] = (6, 3)

        self.print_board_cell_value()
        print(self.elephant_collection)

    def set_goose_initial_position(self):
        count = 1
        for i in range(4, self.nrows, 1):
            for j in range(self.ncols):
                if self.board[i][j].is_valid_cell and self.board[i][j].cell_value is None:
                    self.board[i][j].cell_value = 'G'
                    self.geese_collection['ge_{}'.format(count)] = (i, j)
                    count += 1

        self.print_board_cell_value()
        print(self.geese_collection)

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

    def print_board_cell_value(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                print(self.board[i][j].cell_value, end=" ")
            print("")


board = Board()
# board.set_invalid_points_on_board()
