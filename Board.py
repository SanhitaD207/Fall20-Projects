from Helper import print_board_is_valid, print_board_cell_value


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

        print_board_cell_value(self.board)
        print(self.fox_collection)


    def set_elephant_initial_position(self):
        self.board[4][0].cell_value = 'E'
        self.elephant_collection['ele_1'] = (4, 0)

        self.board[4][6].cell_value = 'E'
        self.elephant_collection['ele_2'] = (4, 6)

        self.board[6][3].cell_value = 'E'
        self.elephant_collection['ele_2'] = (6, 3)

        print_board_cell_value(self.board)
        print(self.elephant_collection)


    def set_goose_initial_position(self):
        count = 1
        for i in range(4, self.nrows, 1):
            for j in range(self.ncols):
                if self.board[i][j].is_valid_cell and self.board[i][j].cell_value is None:
                    self.board[i][j].cell_value = 'G'
                    self.geese_collection['ge_{}'.format(count)] = (i, j)
                    count += 1

        print_board_cell_value(self.board)
        print(self.geese_collection)


    def set_invalid_points_on_board(self):

        for i in range(self.nrows):
            for j in range(self.ncols):
                if (i < 2 or i > 4) and (j < 2 or j > 4):
                    self.board[i][j].is_valid_cell = False
                else:
                    self.board[i][j].is_valid_cell = True

        print_board_is_valid(self.board)


    def get_goose_available_moves(self):
        # TODO - Single cell movement for goose
        # TODO - preference to move that leads to surrounding a fox
        pass


    def get_fox_available_moves(self):
        # TODO - Preference to move that leads to killing goose
        # TODO - Single cell movement if no goose/elephant
        # TODO - Preference to move that leads to surrounding an elephant if close to other fox
        pass


    def get_elephant_available_moves(self):
        # TODO - Single cell movement for elephant
        # TODO - preference to move that leads to surrounding a fox
        pass


board = Board()
# board.set_invalid_points_on_board()
