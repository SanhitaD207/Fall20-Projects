# Set of common utility functions

import numpy as np


def get_single_step_moves(board, row, col):
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = len(board)
    ncols = len(board)

    available_empty_cells = []
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 \
                or not board[r][c].is_valid_cell or board[r][c].cell_value:
            continue
        available_empty_cells.append((r, c))

    return available_empty_cells


def get_hop_moves(board, row, col):
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = len(board)
    ncols = len(board)

    hop_moves = []
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 \
                or not board[r][c].is_valid_cell or board[r][c].cell_value != 'G':
            continue
        diff_i, diff_j = tuple(np.subtract((row, col), (r, c)))

        if diff_i == 0 and diff_j == 1 and c - 1 > -1 and not board[r][c - 1].cell_value:
            hop_moves.append([(r, c - 1), (r, c)])
        elif diff_i == 0 and diff_j == -1 and c + 1 < ncols and not board[r][c + 1].cell_value:
            hop_moves.append([(r, c + 1), (r, c)])
        elif diff_j == 0 and diff_i == 1 and r - 1 > -1 and not board[r - 1][c].cell_value:
            hop_moves.append([(r - 1, c), (r, c)])
        elif diff_j == 0 and diff_i == -1 and r + 1 < nrows and not board[r + 1][c].cell_value:
            hop_moves.append([(r + 1, c), (r, c)])

    return hop_moves


def is_fox_surrounded(board, row, col):
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = len(board)
    ncols = len(board)

    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board[r][c].is_valid_cell:
            continue
        if not board[r][c].cell_value:
            return False

    return True


def is_elephant_surrounded(board, row, col):
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = len(board)
    ncols = len(board)

    fox_count = 0
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 or not board[r][c].is_valid_cell:
            continue
        if fox_count > 1:
            return True
        elif board[r][c].cell_value == 'F':
            fox_count += 1

    return False


def print_board_is_valid(board):
    nrows = len(board)
    ncols = len(board[0])
    for i in range(nrows):
        for j in range(ncols):
            print(board[i][j].is_valid_cell, end="\t")
        print("")


def print_board_cell_value(board):
    nrows = len(board)
    ncols = len(board[0])
    for i in range(nrows):
        for j in range(ncols):
            print(board[i][j].cell_value if board[i][j].cell_value else '_', end="\t")
        print("")
