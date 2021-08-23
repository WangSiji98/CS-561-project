import numpy as np
from data_structure import heapdict

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

def ucs(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list):
    searched_maps = np.zeros([H, W]).astype(np.int32)
    precursor_maps = np.zeros([H, W, 2]).astype(np.int32)
    distance_maps = (np.ones([H, W])*(2**31 -1)).astype(np.int32)
    q = heapdict()

    searched_maps[START_Y, START_X] = 1
    precursor_maps[START_Y, START_X] = [-1, -1]
    distance_maps[START_Y, START_X] = 0
    result = {}
    # cost = {}
    q[START_Y * W + START_X] = 0

    while len(q) > 0:
        current = q.popitem()
        h = np.int32(current[0] / W)
        w = np.int32(current[0] % W)
        searched_maps[h, w] = 1

        if [w, h] in settle_list:
            goal = [w, h]
            route = [[w, h]]
            pointer = [w, h]
            while np.all(precursor_maps[pointer[1], pointer[0]] != [-1, -1]):
                route.append(precursor_maps[pointer[1], pointer[0]].tolist())
                pointer = precursor_maps[pointer[1], pointer[0]].tolist()
            result[goal[1] * W + goal[0]] = list(reversed(route))
            # cost[goal[1] * W + goal[0]] = distance_maps[goal[1], goal[0]]
            settle_list.remove(goal)
            if not settle_list:
                break

        neighbor_hor_ver = [[w + 1, h],
                            [w, h - 1],
                            [w - 1, h],
                            [w, h + 1]
                            ]

        neighbor_dia = [[w + 1, h + 1],
                        [w + 1, h - 1],
                        [w - 1, h - 1],
                        [w - 1, h + 1],
                        ]

        for i in range(4):
            if is_legal(maps, neighbor_hor_ver[i], W, H) and searched_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]] == 0:
                height_diff = np.abs(height(maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]]) - height(maps[h, w]))
                if height_diff <= MAX_ROCK_HEIGHT:
                    if distance_maps[h, w] + 10 < distance_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]]:
                        precursor_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]] = [w, h]
                        distance_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]] = distance_maps[h, w] + 10
                        q[neighbor_hor_ver[i][1] * W + neighbor_hor_ver[i][0]] = distance_maps[h, w] + 10

        for i in range(4):
            if is_legal(maps, neighbor_dia[i], W, H) and searched_maps[neighbor_dia[i][1], neighbor_dia[i][0]] == 0:
                height_diff = np.abs(height(maps[neighbor_dia[i][1], neighbor_dia[i][0]]) - height(maps[h, w]))
                if height_diff <= MAX_ROCK_HEIGHT:
                    if distance_maps[h, w] + 14 < distance_maps[neighbor_dia[i][1], neighbor_dia[i][0]]:
                        precursor_maps[neighbor_dia[i][1], neighbor_dia[i][0]] = [w, h]
                        distance_maps[neighbor_dia[i][1], neighbor_dia[i][0]] = distance_maps[h, w] + 14
                        q[neighbor_dia[i][1] * W + neighbor_dia[i][0]] = distance_maps[h, w] + 14

        searched_maps[h, w] = 1
    return result












