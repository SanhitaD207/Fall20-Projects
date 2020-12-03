from Helper import get_single_step_moves, get_hop_moves, parse_input_move


class Player:
    """
    This is the base player class to define the functions that must be there in any child class that inherits
        this parent Player Class.
    """


    def move(self, board):
        pass


    def move_ai(self, board, animal_collection, board_piece, move):
        pass


    def move_piece(self, board, board_piece, board_piece_final_location, animal_collection=None, is_ai_player=False):
        pass


class GeeseElephantPlayer(Player):
    def __init__(self):
        self.geese_collection = {}
        self.elephant_collection = {}


    def move(self, board):
        """
        This function is called during game-play when we are not using the AI Player, and instead using manual
            input for the moves.
        :param board: Current Board State
        """

        all_moves = self.get_goose_available_moves(board)
        all_moves.update(self.get_elephant_available_moves(board))
        print(self.elephant_collection)
        print(self.geese_collection)
        print("All moves GE:", all_moves)
        print("Geese-Elephant player")
        best_move = input("Enter the best move (format - fox_1 (3,2)) ")
        board_piece, board_piece_final_location = parse_input_move(best_move)
        self.move_piece(board, board_piece, board_piece_final_location)


    def move_ai(self, board, animal_collection, board_piece, move):
        """
        This function is called during game-play when we are using the AI game player with minimax for choosing
            best move.
        :param board: Current Board State
        :param animal_collection: Geese and Elephant Collection combined
        :param board_piece: Board Piece to be moved, for example - ge_1 for Goose 1
        :param move: Where the board piece is to be moved (coordinates), for example - (3,2)
        """

        self.move_piece(board, board_piece, move, animal_collection, True)


    def move_piece(self, board, board_piece, board_piece_final_location, animal_collection=None, is_ai_player=False):
        """
        This function takes in the parameters and makes the move
        :param board: Current Board State
        :param board_piece: Board Piece to be moved, for example - ge_1 for Goose 1
        :param board_piece_final_location: Where the board piece is to be moved (coordinates), for example - (3,2)
        :param animal_collection: Geese and Elephant Collection combined
        :param is_ai_player: Flag value to check if the game player is manual / AI
        """

        if not is_ai_player:
            if 'ge' in board_piece:
                row, col = self.geese_collection[board_piece]
            else:
                row, col = self.elephant_collection[board_piece]
        else:
            row, col = animal_collection[board_piece]

        piece_cell_value = board.board[row][col].cell_value
        board.board[row][col].cell_value = None

        row, col = board_piece_final_location
        board.board[row][col].cell_value = piece_cell_value

        if not is_ai_player:
            if 'ge' in board_piece:
                self.geese_collection[board_piece] = (row, col)
            else:
                self.elephant_collection[board_piece] = (row, col)
        else:
            animal_collection[board_piece] = (row, col)


    def get_goose_available_moves(self, board, geese_collection=None, is_ai_player=False):
        """
        This function is called to fetch all available moves for each goose
        :param board: Current Board State
        :param geese_collection: A dictionary containing the geese board pieces and their locations on the board
        :param is_ai_player: Flag value to check if the game player is manual / AI and accordingly choose the
            right collection
        """

        moves = {}
        available_pieces = geese_collection.items() if is_ai_player else self.geese_collection.items()
        for key, val in available_pieces:
            moves[key] = get_single_step_moves(board, *val)

        return moves


    def get_elephant_available_moves(self, board, elephant_collection=None, is_ai_player=False):
        """
        This function is called to fetch all available moves for each elephant
        :param board: Current Board State
        :param elephant_collection: A dictionary containing the elephant board pieces and their
            locations on the board
        :param is_ai_player: Flag value to check if the game player is manual / AI and accordingly choose the
            right collection
        """

        moves = {}
        available_pieces = elephant_collection.items() if is_ai_player else self.elephant_collection.items()
        for key, val in available_pieces:
            moves[key] = get_single_step_moves(board, *val)
            # print(f'\n{key} available moves: ', moves[key])

        return moves


class FoxPlayer(Player):
    def __init__(self):
        self.fox_collection = {}


    def move(self, board):
        """
        This function is called during game-play when we are not using the AI Player, and instead using manual
            input for the moves.
        :param board: Current Board State
        :return: coordinates for the goose captured
        """
        all_moves = self.get_fox_available_moves(board)
        print(self.fox_collection)
        print("All moves F:", all_moves)
        print("Fox player")
        best_move = input("Enter the best move (format - fox_1 (3,2)) ")
        board_piece, board_piece_final_location = parse_input_move(best_move)
        goose_row, goose_col = self.move_piece(board, board_piece, board_piece_final_location)
        return goose_row, goose_col


    def move_ai(self, board, animal_collection, board_piece, move):
        """
        This function is called during game-play when we are using the AI game player with minimax for choosing
            best move.
        :param board: Current Board State
        :param animal_collection: Fox Collection
        :param board_piece: Board Piece to be moved, for example - fox_1 for Fox 1
        :param move: Where the board piece is to be moved (coordinates), for example - (3,2)
        :return: coordinates for the goose captured
        """

        goose_row, goose_col = self.move_piece(board, board_piece, move, animal_collection, True)
        return goose_row, goose_col


    def move_piece(self, board, board_piece, board_piece_final_location, animal_collection=None, is_ai_player=False):
        """
        This function takes in the parameters and makes the move
        :param board: Current Board State
        :param board_piece: Board Piece to be moved, for example - fox_1 for Fox 1
        :param board_piece_final_location: Where the board piece is to be moved (coordinates), for example - (3,2)
        :param animal_collection: Fox Collection
        :param is_ai_player: Flag value to check if the game player is manual / AI
        """

        if is_ai_player:
            row_initial, col_initial = animal_collection[board_piece]
        else:
            row_initial, col_initial = self.fox_collection[board_piece]

        piece_cell_value = board.board[row_initial][col_initial].cell_value
        board.board[row_initial][col_initial].cell_value = None

        row_final, col_final = board_piece_final_location
        goose_row, goose_col = None, None
        if row_initial == row_final and abs(col_final - col_initial) > 1:
            goose_row = row_initial
            goose_col = int((col_initial + col_final) / 2)
        elif col_initial == col_final and abs(row_final - row_initial) > 1:
            goose_row = int((row_initial + row_final) / 2)
            goose_col = col_initial

        board.board[row_final][col_final].cell_value = piece_cell_value

        if is_ai_player:
            animal_collection[board_piece] = (row_final, col_final)
        else:
            self.fox_collection[board_piece] = (row_final, col_final)

        return goose_row, goose_col


    def get_fox_available_moves(self, board, fox_collection=None, is_ai_player=False):
        """
        This function is called to fetch all available moves for each fox
        :param board: Current Board State
        :param fox_collection: A dictionary containing the fox board pieces and their locations on the board
        :param is_ai_player: Flag value to check if the game player is manual / AI and accordingly choose the
            right collection
        """

        moves = {}
        available_moves = fox_collection.items() if is_ai_player else self.fox_collection.items()
        for key, val in available_moves:
            moves[key] = get_hop_moves(board, *val) + get_single_step_moves(board, *val)

        return moves
