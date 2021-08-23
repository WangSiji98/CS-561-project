from state import State
import numpy as np
from game_startegy import generate_game_tree, min_max


def main():
    file_name = '../test_case/test_0.txt'
    input_file = open(file_name)
    board = np.zeros([8, 8], dtype=str)
    for i in range(8):
        tmp = input_file.readline()
        for j in range(8):
            board[i, j] = tmp[j]
    start_state = State(board, 'BLACK')
    depth = 7
    start_state, _ = generate_game_tree(start_state, depth)
    score, s = min_max(start_state, depth)
    print('depth {}'.format(s.depth))
    print(s.current_player)
    print(s.current_board)
    print('score {}'.format(s.score))
    while (s.last_state):
        s = s.last_state
        print('depth {}'.format(s.depth))
        print(s.current_player)
        print(s.current_board)
        print('score {}'.format(s.score))






if __name__ == '__main__':
        main()