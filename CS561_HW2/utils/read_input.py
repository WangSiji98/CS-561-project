import os
import numpy as np


def read_input(filename):
    input_file = open(filename)
    type_of_game = input_file.readline().strip("\n")
    color = input_file.readline().strip("\n")
    remaining_time = float(np.array(input_file.readline().split())[0])

    board = np.zeros([8, 8], dtype=str)
    for i in range(8):
        tmp = input_file.readline()
        for j in range(8):
            board[i, j] = tmp[j]
    input_file.close()

    return type_of_game, color, remaining_time, board


