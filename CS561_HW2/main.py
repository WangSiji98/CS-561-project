from utils import read_input
from game_startegy import single_move
from state import State
from utils import reverse_player
from state import State
import numpy as np
import os
from utils import read_palydata, update_playdata, count_chessmen, output
from game_startegy import generate_game_tree, min_max, alpha_beta_pruning
import copy

def main():
    type_of_game, color, remaining_time, board = read_input('test_case/game.txt')

    current_state = State(current_board=board, current_player=color)
    current_state.update_score()

    if type_of_game == 'SINGLE':
        next_state_list, next_flag_list = single_move(current_state)
        if next_flag_list:
            chosen_state = next_state_list[0]
            path_list = chosen_state.print_path_in_coordinate()
            output(path_list, 'output.txt')
    elif type_of_game == 'GAME':
        playdata_name = 'playdata.txt'
        if not os.path.exists(playdata_name):
            current_turn = 1
            update_playdata(playdata_name, current_turn)
        elif not os.path.getsize(playdata_name):
            current_turn = 1
            update_playdata(playdata_name, current_turn)
        else:
            current_turn = read_palydata(playdata_name)
            current_turn += 1

        number_of_chessmen = count_chessmen(board)
        depth = 7

        # if current_turn < 8:
        #     depth = 4
        # elif remaining_time < 30:
        #     depth = 4
        # elif number_of_chessmen < 3:
        #     depth = 4
        # else:
        #     depth = 7
        current_state_copy = copy.deepcopy(current_state)
        current_state = generate_game_tree(current_state, depth)
        next_state_list, next_flag_list = single_move(current_state_copy)
        if len(next_state_list) == 1:
            state = next_state_list[0]
            path_list = state.print_path_in_coordinate()
            print(state.current_board)
            output(path_list, 'output.txt')
            update_playdata(playdata_name, current_turn)
        else:
            score, chosen_leaf = alpha_beta_pruning(current_state, depth, -1200, 1200)
            # score, chosen_leaf = min_max(current_state, depth)
            # print(score)
            #
            state = chosen_leaf
            tree_path = [state]
            while state.last_state:
                state = state.last_state
                tree_path.append(state)

            if len(tree_path) == 1:
                state = tree_path[0]
            else:
                state = tree_path[-2]
            path_list = state.print_path_in_coordinate()
            print(state.current_board)
            output(path_list, 'output.txt')
            update_playdata(playdata_name, current_turn)


if __name__ == '__main__':
    main()
