from utils import coordinate

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
        print('the path from last state:')
        path_list = []
        if self.path_flag == 'E':
            path_str = self.path_flag + ' ' + coordinate(self.path_from_last_state[0]) + ' ' + coordinate(self.path_from_last_state[1])
            path_list.append(path_str)
            print(path_str)
        elif self.path_flag == 'J':
            for i in range(len(self.path_from_last_state) - 1):
                path_str = self.path_flag + ' ' + coordinate(self.path_from_last_state[i]) + ' ' + coordinate(self.path_from_last_state[i+1])
                path_list.append(path_str)
                print(path_str)
        return path_list





