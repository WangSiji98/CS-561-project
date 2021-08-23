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

def play(depth, turn):
    file_name = '../test_case/game.txt'
    type_of_game, color, remaining_time, board = read_input(file_name)

    current_state = State(current_board=board, current_player=color)
    current_state.update_score()

    if turn < 15:
        depth = 4
    elif count_chessmen(board) < 3:
        depth = 3

    if type_of_game == 'SINGLE':
        next_state_list, next_flag_list = single_move(current_state)
        if next_flag_list:
            chosen_state = next_state_list[0]
            path_list = chosen_state.print_path_in_coordinate()
            output(path_list, 'output.txt')
    elif type_of_game == 'GAME':
        current_state_copy = copy.deepcopy(current_state)
        current_state = generate_game_tree(current_state, depth)
        next_state_list, next_flag_list = single_move(current_state_copy)
        if len(next_state_list) == 1:
            state = next_state_list[0]
        else:
            score, chosen_leaf = alpha_beta_pruning(current_state, depth, -1200, 1200)
            state = chosen_leaf
            tree_path = [state]
            while state.last_state:
                state = state.last_state
                tree_path.append(state)

            if len(tree_path) == 1:
                state = tree_path[0]
            else:
                state = tree_path[-2]
    board = state.current_board


    game_file = open('../test_case/game.txt', 'w')
    game_file.write('GAME\n')
    game_file.write(reverse_player(color)+'\n')
    game_file.write('100.0\n')
    for i in range(8):
        for j in range(8):
            game_file.write(board[i, j])
        game_file.write('\n')
    game_file.close()
    print(board)


type_of_game, color, remaining_time, board = read_input('../test_case/init.txt')
game_file = open('../test_case/game.txt', 'w')
game_file.write('GAME\n')
game_file.write(reverse_player(color)+'\n')
game_file.write('100.0\n')
for i in range(8):
    for j in range(8):
        game_file.write(board[i, j])
    game_file.write('\n')
game_file.close()


for trun in range(120):
    print('current turn:{}'.format(trun))
    print('BLACK')
    play(6, trun)
    print('WHITE')
    play(5, trun)
