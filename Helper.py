# Set of common utility functions

import numpy as np


def get_single_step_moves(board, row, col):
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
    nrows = len(board)
    ncols = len(board[0])

    for i in range(nrows):
        for j in range(ncols):
            print(board[i][j].is_valid_cell, end='\t')
        print('')
    print('')


def print_board_cell_value(board):
    nrows = len(board)
    ncols = len(board[0])

    for i in range(nrows):
        for j in range(ncols):
            print(board[i][j].cell_value if board[i][j].cell_value else '_', end='\t')
        print('')
    print('')


def parse_input_move(move):
    board_piece = move.split(" ")[0]
    board_piece_final_location = (int(move.split(" ")[1][1]), int(move.split(" ")[1][3]))
    return board_piece, board_piece_final_location


def remove_dead_animal(board, row, col, animal_collection):
    board.board[row][col].cell_value = None
    val = (row, col)
    required_key = None
    for key, value in animal_collection.items():
        if val == value:
            required_key = key
            print("Animal found", key)
    animal_collection.pop(required_key, None)
    print(animal_collection)
    print_board_cell_value(board.board)


def remove_dead_foxes_and_elephants(board, fox_collection, elephant_collection):
    for fox_row, fox_col in list(fox_collection.values()):
        if is_fox_surrounded(board, fox_row, fox_col):
            remove_dead_animal(board, fox_row, fox_col, fox_collection)

    for ele_row, ele_col in list(elephant_collection.values()):
        if is_elephant_surrounded(board, ele_row, ele_col):
            remove_dead_animal(board, ele_row, ele_col, elephant_collection)
