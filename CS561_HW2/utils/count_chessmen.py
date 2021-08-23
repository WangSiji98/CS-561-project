

def count_chessmen(board):
    number_of_chessmen = 0
    for row in range(8):
        for column in range(8):
            if board[row, column] != '.':
                number_of_chessmen += 1
    return number_of_chessmen

