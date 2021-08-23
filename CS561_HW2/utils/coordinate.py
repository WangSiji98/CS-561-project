def coordinate(position):
    """
    find coordinate on the board

    :param position: position [row, column]
    :return:
    """
    row, column = position
    return str(chr(ord('a') + column))+str(8 - row)