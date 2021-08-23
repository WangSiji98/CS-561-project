from game_startegy import chessmen_move
from state import State
from utils import reverse_player


def single_move(current_state):
    current_board = current_state.current_board
    color = current_state.current_player[0].lower()
    next_state_list = []
    next_flag_list = []
    final_state_list = []
    final_flag_list = []

    jump_flag = False
    for row in range(8):
        for column in range(8):
            if current_board[row, column].lower() == color:
                tmp_state_list, tmp_flag_list = chessmen_move(current_state, [row, column])
                next_state_list += tmp_state_list
                next_flag_list += tmp_flag_list

    # if next player have nothing can do, we set current player highest(or lowest) score
    # nothing is bigger than winning or losing
    if not next_state_list:
        if current_state.current_player == 'BLACK':
            current_state.score = -128
        else:
            current_state.score = 128

    # check is it possible to jump
    for i in range(len(next_state_list)):
        if next_flag_list[i] == 'J':
            next_state_list[i].path_flag = 'J'
            final_state_list.append(next_state_list[i])
            final_flag_list.append(next_flag_list[i])
            jump_flag = True
        else:
            next_state_list[i].path_flag = 'E'

    # if we can jump, we must choose one of jump path
    if jump_flag:
        current_state.next_state = final_state_list
    else:
        final_state_list = next_state_list
        final_flag_list = next_flag_list

    # set child state depth +1
    for state in next_state_list:
        state.depth = current_state.depth + 1

    current_state.next_state = final_state_list

    return final_state_list, final_flag_list



