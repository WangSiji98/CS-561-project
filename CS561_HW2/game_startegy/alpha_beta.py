from state import State
import sys


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






