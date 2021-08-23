import numpy as np
import os


def read_palydata(file_name):
    time_file = open(file_name)
    current_turn = np.array(time_file.readline().split())[0].astype(np.int)
    time_file.close()

    return current_turn


def update_playdata(file_name, current_turn):
    time_file = open(file_name, 'w')
    time_file.write(str(current_turn))