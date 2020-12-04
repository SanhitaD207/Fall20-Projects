# Set of common utility functions

import numpy as np


def get_single_step_moves(board, row, col):
    """
    Returns all possible single step moves (top, bottom, left, right) for the board piece with row and col as its current
    coordinate
    :param board: Current Board State
    :param row: Integer denoting the row coordinate of the board piece
    :param col: Integer denoting the column coordinate of the board piece
    :return: List of tuples where each tuple denotes the final coordinate of the board piece after the move
    """
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = board.nrows
    ncols = board.ncols

    available_empty_cells = []
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 \
                or not board.board[r][c].is_valid_cell or board.board[r][c].cell_value:
            continue
        available_empty_cells.append((r, c))

    return available_empty_cells


def get_hop_moves(board, row, col):
    """
    Returns all possible moves that can make it possible for the fox to capture a goose by hopping over it.
    :param board: Current Board State
    :param row: Integer denoting the row coordinate of the board piece
    :param col: Integer denoting the column coordinate of the board piece
    :return: List of tuples where each tuple denotes the final coordinate of the board piece after the move
    """
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = board.nrows
    ncols = board.ncols

    hop_moves = []
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 \
                or not board.board[r][c].is_valid_cell or board.board[r][c].cell_value != 'G':
            continue
        diff_i, diff_j = tuple(np.subtract((row, col), (r, c)))

        if diff_i == 0 and diff_j == 1 and c - 1 > -1 and not board.board[r][c - 1].cell_value and \
                board.board[r][c - 1].is_valid_cell:
            hop_moves.append((r, c - 1))
        elif diff_i == 0 and diff_j == -1 and c + 1 < ncols and not board.board[r][c + 1].cell_value and \
                board.board[r][c + 1].is_valid_cell:
            hop_moves.append((r, c + 1))
        elif diff_j == 0 and diff_i == 1 and r - 1 > -1 and not board.board[r - 1][c].cell_value and \
                board.board[r - 1][c].is_valid_cell:
            hop_moves.append((r - 1, c))
        elif diff_j == 0 and diff_i == -1 and r + 1 < nrows and not board.board[r + 1][c].cell_value and \
                board.board[r + 1][c].is_valid_cell:
            hop_moves.append((r + 1, c))

    return hop_moves


def is_fox_surrounded(board, row, col):
    """
    Used to check if the fox is blocked in all direction and is unable to move. Conditions when the fox is not blocked is
    when it has an empty cell next to it, when it can hop over a goose next to it and when a fox is next to it.
    :param board: Current Board State
    :param row: Integer denoting the row coordinate of the board piece
    :param col: Integer denoting the column coordinate of the board piece
    :return: Boolean value indicating whether the fox is surrounded
    """
    if not get_single_step_moves(board, row, col) and not get_hop_moves(board, row, col):
        adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

        nrows = board.nrows
        ncols = board.ncols

        for r, c in adjacent_coordinates:
            if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board.board[r][c].is_valid_cell:
                continue
            if board.board[r][c].cell_value == 'F':
                return False

        return True

    return False


def is_elephant_surrounded(board, row, col):
    """
    Used to check if the elephant is surrounded by foxes. An elephant is considered surrounded if there are two foxes in its
    periphery by occupying top/bottom/left/right cells.
    :param board: Current Board State
    :param row: Integer denoting the row coordinate of the board piece
    :param col: Integer denoting the column coordinate of the board piece
    :return: Boolean value indicating whether the elephant is surrounded
    """
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = board.nrows
    ncols = board.ncols

    fox_count = 0
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board.board[r][c].is_valid_cell:
            continue
        elif board.board[r][c].cell_value == 'F':
            fox_count += 1
            if fox_count > 1:
                return True

    return False


def print_board_is_valid(board):
    """
    Prints the is_valid_cell parameters of the cells on the board
    :param board: Game board
    """
    nrows = len(board)
    ncols = len(board[0])

    for i in range(nrows):
        for j in range(ncols):
            print(board[i][j].is_valid_cell, end='\t')
        print('')
    print('')


def print_board_cell_value(board):
    """
    Prints the cell_value parameter of the cells on the board
    :param board: Game board
    """
    nrows = len(board)
    ncols = len(board[0])

    for i in range(nrows):
        for j in range(ncols):
            if not board[i][j].is_valid_cell:
                print('X', end='\t')
            else:
                print(board[i][j].cell_value if board[i][j].cell_value else '_', end='\t')
        print('')
    print('\n\n')


def parse_input_move(move):
    """
    Used to split the input into board piece and that board pieces final location
    :param move: A string containing the move provided by the user
    :return board_piece: A string containing the name of the board piece to be moved
    :return board_piece_final_location: A tuple containing the final coordinates of the board piece after the move
    """
    board_piece = move.split(" ")[0]
    board_piece_final_location = (int(move.split(" ")[1][1]), int(move.split(" ")[1][3]))
    return board_piece, board_piece_final_location


def remove_dead_animal(board, row, col, animal_collection):
    """
    Removes the captured animal from the board and its corresponding animal collection
    :param board: Current Board State
    :param row: Integer denoting the row coordinate of the board piece
    :param col: Integer denoting the column coordinate of the board piece
    :param animal_collection: A dictionary containing the board pieces and their locations on the board
    """
    board.board[row][col].cell_value = None
    val = (row, col)
    required_key = None
    for key, value in animal_collection.items():
        if val == value:
            required_key = key
            break
    animal_collection.pop(required_key, None)


def remove_dead_foxes_and_elephants(board, fox_collection, elephant_collection):
    """
    Removes the foxes and elephants from the game if either of them are surrounded
    :param board: Current Board State
    :param fox_collection: A dictionary containing the fox board pieces and their locations on the board
    :param elephant_collection: A dictionary containing the elephant board pieces and their locations on the board
    """
    for fox_row, fox_col in list(fox_collection.values()):
        if is_fox_surrounded(board, fox_row, fox_col):
            remove_dead_animal(board, fox_row, fox_col, fox_collection)

    for ele_row, ele_col in list(elephant_collection.values()):
        if is_elephant_surrounded(board, ele_row, ele_col):
            remove_dead_animal(board, ele_row, ele_col, elephant_collection)
