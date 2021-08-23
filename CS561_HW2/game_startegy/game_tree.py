from game_startegy import single_move

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



