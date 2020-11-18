# Set of common utility functions


def get_adjacent_empty_cells(board, row, col):
    adjacent_coordinates = [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)]

    nrows = len(board)
    ncols = len(board)

    available_empty_cells = []
    for r, c in adjacent_coordinates:
        if r > nrows - 1 or c > ncols - 1 or r < 0 or c < 0 \
                or not board[r][c].is_valid_cell or not board[r][c].cell_value:
            continue
        available_empty_cells.append((r, c))

    return available_empty_cells


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
