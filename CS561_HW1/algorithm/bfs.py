import numpy as np
from queue import Queue

def is_legal(maps, coordinate, W, H):
    if coordinate[0] >= 0 and coordinate[0] < W and coordinate[1] >= 0 and coordinate[1] < H:
        return True
    else:
        return False

def height(mud):
    if mud < 0:
        return np.abs(mud)
    else:
        return np.int32(0)

def bfs(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list):
    searched_maps = np.zeros([H, W]).astype(np.int32)
    precursor_maps = np.zeros([H, W, 2]).astype(np.int32)
    q = Queue()
    q.put([START_X, START_Y])
    searched_maps[START_Y, START_X] = 1
    precursor_maps[START_Y, START_X] = [-1, -1]
    result = {}

    while not q.empty():
        current = q.get()
        if current in settle_list:
            goal = current
            route = [current]
            pointer = current
            while np.all(precursor_maps[pointer[1], pointer[0]] != [-1, -1]):
                route.append(precursor_maps[pointer[1], pointer[0]].tolist())
                pointer = precursor_maps[pointer[1], pointer[0]].tolist()
            result[goal[1] * W + goal[0]] = list(reversed(route))
            settle_list.remove(goal)
            if not settle_list:
                break

        neighbor = [[current[0] + 1, current[1] + 1],
                    [current[0] + 1, current[1]],
                    [current[0] + 1, current[1] - 1],
                    [current[0], current[1] - 1],
                    [current[0] - 1, current[1] - 1],
                    [current[0] - 1, current[1]],
                    [current[0] - 1, current[1] + 1],
                    [current[0], current[1] + 1]
                    ]
        for i in range(8):
            if is_legal(maps, neighbor[i], W, H) and searched_maps[neighbor[i][1], neighbor[i][0]] == 0:
                height_diff = np.abs(height(maps[neighbor[i][1], neighbor[i][0]]) - height(maps[current[1], current[0]]))
                if height_diff <= MAX_ROCK_HEIGHT:
                    searched_maps[neighbor[i][1], neighbor[i][0]] = 1
                    precursor_maps[neighbor[i][1], neighbor[i][0]] = current
                    q.put(neighbor[i])
        searched_maps[current[1], current[0]] = 2

    return result