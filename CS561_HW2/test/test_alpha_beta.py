from state import State
import numpy as np
from game_startegy import generate_game_tree, min_max, alpha_beta_pruning
from utils import read_input


def main():
    type_of_game, color, remaining_time, board = read_input('../test_case/test_0.txt')
    start_state = State(board, 'BLACK')
    depth = 8
    start_state, _ = generate_game_tree(start_state, depth)
    score, s = alpha_beta_pruning(start_state, depth, -128, 128)
    while (depth > 1):
        s = s.last_state
        depth -= 1

    print('depth {}'.format(s.depth))
    print(s.current_player)
    print(s.current_board)
    print('score {}'.format(s.score))
    s.print_path_in_coordinate()










if __name__ == '__main__':
        main()