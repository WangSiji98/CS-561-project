from state import State
import sys


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
