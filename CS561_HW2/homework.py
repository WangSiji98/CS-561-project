from utils import coordinate
import numpy as np
import os
import sys
import copy
from queue import Queue
import time


class State():
    def __init__(self, current_board, current_player=None, last_state=None, next_state=[], path_from_last_state=[], path_flag='', score=0, flag_from_last_state='', depth=0):
        self.current_board = current_board
        self.current_player = current_player
        self.last_state = last_state
        self.next_state = next_state
        self.path_from_last_state = path_from_last_state
        self.path_flag = path_flag
        self.score = score
        self.flag_from_last_state = flag_from_last_state
        self.depth = depth

    def __lt__(self, rhs):
        return self.score < rhs.score

    def __le__(self, rhs):
        return self.score <= rhs.score

    def __gt__(self, rhs):
        return self.score > rhs.score

    def __ge__(self, rhs):
        return self.score >= rhs.score

    def __eq__(self, rhs):
        return self.score == rhs.score

    def __ne__(self, rhs):
        return self.score != rhs.score

    def print_board(self):
        print(self.current_board)

    def get_board(self):
        return self.current_board

    def reverse_player(self):
        if self.current_player.lower() == 'w':
            return 'b'
        else:
            return 'w'

    def update_score(self):
        no_white_flag = True
        no_black_flag = True
        self.score = 0
        for row in range(8):
            for column in range(8):
                if self.current_board[row, column] == 'b':
                    no_black_flag = False
                    self.score += 1
                elif self.current_board[row, column] == 'B':
                    no_black_flag = False
                    self.score += 2
                elif self.current_board[row, column] == 'w':
                    no_white_flag = False
                    self.score -= 1
                elif self.current_board[row, column] == 'W':
                    no_white_flag = False
                    self.score -= 2
        if no_black_flag:
            self.score = -128
        elif no_white_flag:
            self.score = 128

    def print_score(self):
        print('score:{}'.format(self.score))

    def get_score(self):
        return self.score

    def update_path(self, position):
        self.path_from_last_state.append(position)

    def get_path(self):
        return self.path_from_last_state

    def print_path(self):
        print(self.path_from_last_state)

    def print_path_in_coordinate(self):
        # print('the path from last state:')
        path_list = []
        if self.path_flag == 'E':
            path_str = self.path_flag + ' ' + coordinate(self.path_from_last_state[0]) + ' ' + coordinate(self.path_from_last_state[1])
            path_list.append(path_str)
            # print(path_str)
        elif self.path_flag == 'J':
            for i in range(len(self.path_from_last_state) - 1):
                path_str = self.path_flag + ' ' + coordinate(self.path_from_last_state[i]) + ' ' + coordinate(self.path_from_last_state[i+1])
                path_list.append(path_str)
                # print(path_str)
        return path_list


def reverse_player(current_player):
    """
    to reverse the player, if it is black, then we reverse it to white.

    :param current_player: the current player(color, king or man)
    :return: reversed player
    """

    if current_player == 'BLACK':
        next_player = 'WHITE'
    else:
        next_player = 'BLACK'
    return next_player


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


def read_palydata(file_name):
    time_file = open(file_name)
    current_turn = np.array(time_file.readline().split())[0].astype(np.int)
    last_remaining_time = float(np.array(time_file.readline().split())[0])
    total_time = float(np.array(time_file.readline().split())[0])
    time_file.close()

    return current_turn, last_remaining_time, total_time


def update_playdata(file_name, current_turn, last_remaining_time, total_time):
    time_file = open(file_name, 'w')
    time_file.write(str(current_turn) + '\n')
    time_file.write(str(last_remaining_time) + '\n')
    time_file.write(str(total_time) + '\n')


def output(path_list, output_file_name):
    output_file = open(output_file_name, 'w')
    for path_str in path_list:
        output_file.write(path_str)
        output_file.write('\n')
    output_file.close()


def count_chessmen(board):
    number_of_chessmen = 0
    for row in range(8):
        for column in range(8):
            if board[row, column] != '.':
                number_of_chessmen += 1
    return number_of_chessmen


def coordinate(position):
    """
    find coordinate on the board

    :param position: position [row, column]
    :return:
    """
    row, column = position
    return str(chr(ord('a') + column))+str(8 - row)


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


def chessmen_move(current_state, position):
    row, column = position
    current_board = current_state.current_board
    current_chessmen = current_board[row, column]
    next_position = direction(current_chessmen, [row, column])

    next_state_list = []
    final_state_list = []
    flag_list = []
    final_flag_list = []
    jump_flag = False

    for p in next_position:
        current_state, tmp_next_state_list, tmp_flag = move_one_direction(current_state, position, p)
        next_state_list += tmp_next_state_list

        if tmp_flag != 'J' and tmp_flag != 'E':
            continue
        elif len(tmp_next_state_list) > 1:
            for _ in range(len(tmp_next_state_list)):
                flag_list.append(tmp_flag)
        else:
            flag_list.append(tmp_flag)

    for i in range(len(next_state_list)):
        if flag_list[i] == 'J':
            final_state_list.append(next_state_list[i])
            final_flag_list.append(flag_list[i])
            jump_flag = True

    if jump_flag:
        return final_state_list, final_flag_list
    else:
        return next_state_list, flag_list


def move_one_direction(current_state, position, next_position):
    row, column = position
    next_row, next_column = next_position
    current_board = current_state.current_board
    # current state is finished, next state should reverse player
    current_color = current_state.current_player[0].lower()
    current_chessmen = current_board[row, column] # choose the chessmen we want wo move

    # next position out of boundary
    if not boundary_detection(next_position):
        flag = 'I_N'
        return current_state, [], flag

    # next position is same color chessmen
    if current_board[next_row, next_column].lower() == current_color:
        flag = 'S'
        return current_state, [], flag

    # E move diagonally
    elif current_board[next_row, next_column].lower() == '.':
        tmp_board = current_board.copy() # copy board
        tmp_board[row, column] = '.'
        # judge whether the chessmen is king
        _, current_chessmen = king(current_chessmen, [next_row, next_column])
        tmp_board[next_row, next_column] = current_chessmen
        flag = 'E'
        # final state should reverse player
        final_state = State(current_board=tmp_board, current_player=reverse_player(current_state.current_player), last_state=current_state, path_from_last_state=[position, [next_row, next_column]])
        final_state.update_score()
        return current_state, [final_state], flag

    # J single jump/continuous_jump
    elif current_board[next_row, next_column].lower() != current_color and current_board[next_row, next_column].lower() != '.':
        jump_row = 2 * next_row - row
        jump_column = 2 * next_column - column

        # jump position out of boundary
        if not boundary_detection([jump_row, jump_column]) or current_board[jump_row, jump_column].lower() != '.':
            flag = 'I_J'
            return current_state, [], flag

        flag = 'J'
        king_flag, current_chessmen = king(current_chessmen, [jump_row, jump_column])
        tmp_board = current_board.copy()
        tmp_board[row, column] = '.'
        tmp_board[next_row, next_column] = '.'
        tmp_board[jump_row, jump_column] = current_chessmen
        next_state = State(current_board=tmp_board, current_player=current_state.current_player, last_state=current_state, path_from_last_state=[position, [jump_row, jump_column]])
        next_state.update_score()
        # if the chessmen become king, it should stop
        if king_flag:
            next_state.current_player = reverse_player(next_state.current_player)
            return current_state, [next_state], flag
        else:
            # if not, we should detect continuous jump
            final_state_list = continuous_jump(next_state, [jump_row, jump_column], current_chessmen)
            if final_state_list:
                # set all final state's last state as current state
                for i in range(len(final_state_list)):
                    final_state_list[i].last_state = current_state
            return current_state, final_state_list, flag


def continuous_jump(state, position, current_chessmen):
    """
    use BFS to search the continuous jump after one jump
    """
    # BFS Queue
    search_queue = Queue()
    search_queue.put([state, position])
    final_state_list = []

    while not search_queue.empty():
        current_state, current_position = search_queue.get()
        row, column = current_position
        next_position = direction(current_chessmen, current_position)
        current_board = current_state.current_board
        current_path = current_state.path_from_last_state
        current_queue_size = search_queue.qsize()
        child_flag = False

        for p in next_position:
            next_row, next_column = p
            if not boundary_detection(p):
                continue
            # only jump is allowed, move diagonally is not
            if current_board[next_row, next_column].lower() != current_chessmen.lower() and current_board[next_row, next_column].lower() != '.':
                jump_row = 2 * next_row - row
                jump_column = 2 * next_column - column
                if not boundary_detection([jump_row, jump_column]) or current_board[jump_row, jump_column].lower() != '.':
                    continue
                king_flag, current_chessmen = king(current_chessmen, [jump_row, jump_column])
                tmp_board = current_board.copy()
                tmp_board[row, column] = '.'
                tmp_board[next_row, next_column] = '.'
                tmp_board[jump_row, jump_column] = current_chessmen
                # regard continuous jump as one move, but we still need to record path
                next_state = State(current_board=tmp_board, current_player=current_state.current_player, last_state=current_state, path_from_last_state=current_path[:])
                next_state.update_score()
                # update path
                next_state.update_path([jump_row, jump_column])
                if king_flag:
                    final_state_list.append(next_state)
                    # final state should reverse player
                    next_state.current_player = reverse_player(next_state.current_player)
                    child_flag = True
                else:
                    search_queue.put([next_state, [jump_row, jump_column]])
        # if it could not jump continuously, we should set current position as final position
        if search_queue.qsize() == current_queue_size and not child_flag:
            # final state should reverse player
            current_state.current_player = reverse_player(current_state.current_player)
            final_state_list.append(current_state)

    return final_state_list


def boundary_detection(position):
    """
    boundary_detection

    :param position: input is list [row, column] for position, the board is 8*8
    :return: T or F
    """
    row, column = position
    if row < 0 or row > 7 or column < 0 or column > 7:
        return False
    else:
        return True


def direction(current_chessmen, position):
    """
    to find the possible next move direction for the chessmen accroding its type

    :param current_chessmen: type of chessmen(color, king or man)
    :param position: the current position of the chessmen
    :return: possible direction
    """
    row, column = position
    all_direction = [[row + 1, column - 1],
                 [row + 1, column + 1],
                 [row - 1, column - 1],
                 [row - 1, column + 1]
                 ]
    if current_chessmen == 'b':
        possible_direction = all_direction[0:2]
    elif current_chessmen == 'w':
        possible_direction = all_direction[2:4]
    else:
        possible_direction = all_direction
    return possible_direction


def king(current_chessmen, position):
    """
    to promote one man who arrives the bottom line on the opposite side to a king

    :param current_chessmen: type of chessmen(color, king or man)
    :param position: the current position of the chessmen
    :return: promotion or not
    """
    king_flag = False
    row, _ = position
    if current_chessmen == 'b' and row == 7:
        current_chessmen = 'B'
        king_flag = True
    elif current_chessmen == 'w' and row == 0:
        current_chessmen = 'W'
        king_flag = True
    return king_flag, current_chessmen


def min_max(state, depth):
    chosen_state = None

    if state.depth == depth or state.score == 128 or state.score == -128:
        return state.score, state

    if state.current_player == 'BLACK':
        score = -128
        for child_state in state.next_state:
            child_score, child = min_max(child_state, depth)
            # print(child_score)
            # print(child.current_board)
            if score < child_score:
                # print('yes')
                score = child_score
                chosen_state = child
    else:
        score = 128
        for child_state in state.next_state:
            child_score, child = min_max(child_state, depth)
            if score > child_score:
                score = child_score
                chosen_state = child
    return score, chosen_state


def alpha_beta_pruning(state, depth, alpha, beta):
    chosen_state = None

    if state.depth == depth or state.score == 128 or state.score == -128:
        return state.score, state

    if state.current_player == 'BLACK':
        score = -129
        for child_state in state.next_state:
            child_score, child = alpha_beta_pruning(child_state, depth, alpha, beta)
            if score < child_score:
                score = child_score
                chosen_state = child
            if score >= beta:
                    return score, chosen_state
            if score > alpha:
                alpha = score
    else:
        score = 129
        for child_state in state.next_state:
            child_score, child = alpha_beta_pruning(child_state, depth, alpha, beta)
            if score > child_score:
                score = child_score
                chosen_state = child
            if score <= alpha:
                    return score, chosen_state
            if score < beta:
                beta = score

    return score, chosen_state


def generate_game_tree(start_state, depth):
    current_state_list = [start_state]
    game_tree_list = []
    game_tree_list.append(current_state_list)

    for i in range(depth):
        result_state_list = []
        for state in current_state_list:
            tmp_list, _ = single_move(state)
            result_state_list += tmp_list
        current_state_list = result_state_list
        game_tree_list.append(result_state_list)

    return start_state


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
            last_remaining_time = remaining_time
            total_time = remaining_time
            update_playdata(playdata_name, current_turn, last_remaining_time, total_time)
        elif not os.path.getsize(playdata_name):
            current_turn = 1
            last_remaining_time = remaining_time
            total_time = remaining_time
            update_playdata(playdata_name, current_turn, last_remaining_time, total_time)
        else:
            current_turn, last_remaining_time, total_time = read_palydata(playdata_name)
            current_turn += 1

        last_time_cost = last_remaining_time - remaining_time
        number_of_chessmen = count_chessmen(board)

        depth = 6
        print(count_chessmen(board))

        if current_turn <= 5:
            depth = 4
        elif current_turn > 5 and current_turn <= 10:
            depth = 5
        else:
            depth = 6

        if number_of_chessmen <= 8 and number_of_chessmen > 4:
            depth = 5
        elif number_of_chessmen <= 4:
            depth = 4

        if last_time_cost / total_time >= 0.05 and last_time_cost / total_time < 0.1:
            depth -= 1
        elif last_time_cost / total_time >= 0.1:
            depth -= 2

        if remaining_time < 30:
            depth = 3

        print(depth)

        current_state_copy = copy.deepcopy(current_state)
        current_state = generate_game_tree(current_state, depth)
        next_state_list, next_flag_list = single_move(current_state_copy)
        if len(next_state_list) == 1:
            state = next_state_list[0]
            path_list = state.print_path_in_coordinate()
            # print(state.current_board)
            output(path_list, 'output.txt')
            update_playdata(playdata_name, current_turn, remaining_time, total_time)
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
            path_list = state.print_path_in_coordinate()
            print(state.current_board)
            output(path_list, 'output.txt')
            update_playdata(playdata_name, current_turn, remaining_time, total_time)


if __name__ == '__main__':
    main()





