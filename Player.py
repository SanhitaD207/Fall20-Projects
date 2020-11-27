from Helper import get_single_step_moves, get_hop_moves, parse_input_move, print_board_cell_value


class Player:
    def move(self, board):
        pass


class GeeseElephantPlayer(Player):
    def __init__(self):
        self.geese_collection = {}
        self.elephant_collection = {}

    def move(self, board):
        all_moves = self.get_goose_available_moves(board)
        all_moves.update(self.get_elephant_available_moves(board))
        print(self.elephant_collection)
        print(self.geese_collection)
        print("All moves GE:", all_moves)
        print("Geese-Elephant player")
        best_move = input("Enter the best move (format - fox_1 (3,2)) ")
        board_piece, board_piece_final_location = parse_input_move(best_move)
        self.move_piece(board, board_piece, board_piece_final_location)
        print_board_cell_value(board.board)

    def move_piece(self, board, board_piece, board_piece_final_location):
        if 'ge' in board_piece:
            row, col = self.geese_collection[board_piece]
        else:
            row, col = self.elephant_collection[board_piece]

        piece_cell_value = board.board[row][col].cell_value
        board.board[row][col].cell_value = None

        row, col = board_piece_final_location
        board.board[row][col].cell_value = piece_cell_value

        if 'ge' in board_piece:
            self.geese_collection[board_piece] = (row, col)
        else:
            self.elephant_collection[board_piece] = (row, col)

    def get_goose_available_moves(self, board):
        moves = {}
        for key, val in self.geese_collection.items():
            moves[key] = get_single_step_moves(board, *val)
            # print(f'\n{key} available moves: ', moves[key])

        return moves

    def get_elephant_available_moves(self, board):
        moves = {}
        for key, val in self.elephant_collection.items():
            moves[key] = get_single_step_moves(board, *val)
            # print(f'\n{key} available moves: ', moves[key])

        return moves


class FoxPlayer(Player):
    def __init__(self):
        self.fox_collection = {}

    def move(self, board):
        all_moves = self.get_fox_available_moves(board)
        print(self.fox_collection)
        print("All moves F:", all_moves)
        print("Fox player")
        best_move = input("Enter the best move (format - fox_1 (3,2)) ")
        board_piece, board_piece_final_location = parse_input_move(best_move)
        goose_row, goose_col = self.move_piece(board, board_piece, board_piece_final_location)
        print_board_cell_value(board.board)
        return goose_row, goose_col

    def move_piece(self, board, board_piece, board_piece_final_location):

        row_initial, col_initial = self.fox_collection[board_piece]

        piece_cell_value = board.board[row_initial][col_initial].cell_value
        board.board[row_initial][col_initial].cell_value = None

        row_final, col_final = board_piece_final_location
        goose_row, goose_col = None, None
        if row_initial == row_final and abs(col_final - col_initial) > 1:
            print("Fox hopped in row")
            goose_row = row_initial
            goose_col = int((col_initial + col_final) / 2)
        elif col_initial == col_final and abs(row_final - row_initial) > 1:
            print("Fox hopped in column")
            goose_row = int((row_initial + row_final) / 2)
            goose_col = col_initial

        board.board[row_final][col_final].cell_value = piece_cell_value
        self.fox_collection[board_piece] = (row_final, col_final)
        return goose_row, goose_col

    def get_fox_available_moves(self, board):
        moves = {}
        for key, val in self.fox_collection.items():
            moves[key] = get_hop_moves(board, *val) + get_single_step_moves(board, *val)
            # print(f'\n{key} available moves: ', moves[key])

        return moves
