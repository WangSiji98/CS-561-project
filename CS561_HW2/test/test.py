from state import State
import numpy as np
from game_startegy import single_move

def main():
    file_name = '../test_case/test_1.txt'
    input_file = open(file_name)
    board = np.zeros([8, 8], dtype=str)
    for i in range(8):
        tmp = input_file.readline()
        for j in range(8):
            board[i, j] = tmp[j]
    s = State(board, 'WHITE')
    c, f = single_move(s)
    print(s.score)
    for state in c:
        print(state.current_board)
    # print('parent')
    # print(s.current_board)
    # print('child')
    # for state in s.next_state:
    #     print(state.current_board)





    # print('depth 0')
    # print(s.current_player)
    # print(s.current_board)
    # for state in c:
    #     print('depth 1')
    #     print(state.current_player)
    #     print(state.current_board)
    #     c1, _ = single_move(state)
    #     for state1 in c1:
    #         print('depth 2')
    #         print(state1.current_player)
    #         print(state1.current_board)

    # s[0].print_path_in_coordinate(f[0])
    # print(f)
    # for i in range(len(s)):
    #     # print(s[i].depth)
    #     print('last player:{}'.format(s[i].last_state.current_player))
    #     print(s[i].last_state.current_board)
    #     print('current player:{}'.format(s[i].current_player))
    #     print(s[i].current_board)
    #     s[i].print_path_in_coordinate(f[i])
    #     s[i].print_score()


    # print(len(s[0].last_state.next_state))


    # s = sorted(s, reverse=True)
    # for i in range(len(s)):
    #     print(s[i].score)


    # # c, l, f = move_one_direction(s, 'B', [1, 1], [2, 2])
    # # for i in range(len(l)):
    # #     print('parent')
    # #     print(l[i].last_state.current_board)
    # #     print('children')
    # #     print(l[i].current_board)
    # n, f = chessmen_move(s, [1, 1])
    # for i in range(len(n)):
    #     print(n[i].current_board)
    #     n[i].print_path_in_coordinate(f[i])
        # n[i].print_score()
        # print(f[i])
    # s.update_score()
    # s.print_score()


if __name__ == '__main__':
    main()
