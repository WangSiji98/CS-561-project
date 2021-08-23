
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