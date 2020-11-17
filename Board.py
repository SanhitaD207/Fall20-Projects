
class Board:

    def __init__(self):
        self.nrows = 7
        self.ncols = 7

    def set_invalid_points_on_board(self):
        print(self.nrows)


board = Board()
board.set_invalid_points_on_board()