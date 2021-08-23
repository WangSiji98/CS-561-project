from state import State
import numpy as np
from game_startegy import single_move, generate_game_tree

def main():
    file_name = '../test_case/test_0.txt'
    input_file = open(file_name)
    board = np.zeros([8, 8], dtype=str)
    for i in range(8):
        tmp = input_file.readline()
        for j in range(8):
            board[i, j] = tmp[j]
    start_state = State(board, 'WHITE')
    depth = 4
    start_state, tree = generate_game_tree(start_state, depth)

    # print('depth {}'.format(s.depth))
    # print(s.current_player)
    # print(s.current_board)
    # print(s.score)
    # while(s.next_state):
    #     s = s.next_state[0]
    #     print('depth {}'.format(s.depth))
    #     print(s.current_player)
    #     print(s.current_board)
    #     print(s.score)


    # e = l[0]
    # print(e.current_player)
    # print(e.current_board)
    # while(e.last_state):
    #     e = e.last_state
    #     print(e.current_player)
    #     print(e.current_board)

    # print('depth {}'.format(0))
    # print(s.current_board)
    # for depth in range(depth):
    #     print('depth {}'.format(depth+1))
    #     c = s.next_state[0]
    #     print(c.current_player)
    #     # print(c.current_board)
    #     # c.print_path_in_coordinate


if __name__ == '__main__':
        main()