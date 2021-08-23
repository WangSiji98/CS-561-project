from enum import Enum
from state import State
from queue import Queue
from utils import reverse_player


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






