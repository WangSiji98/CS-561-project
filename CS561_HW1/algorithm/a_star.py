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


def muddiness(mud):
    if mud > 0:
        return mud
    else:
        return np.int32(0)


def a_star(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list):
    result = {}
    # cost = {}

    while settle_list:
        searched_maps = np.zeros([H, W]).astype(np.int32)
        precursor_maps = np.zeros([H, W, 2]).astype(np.int32)
        cost_maps = (np.ones([H, W]) * (2 ** 31 - 1)).astype(np.int32)

        searched_maps[START_Y, START_X] = 1
        precursor_maps[START_Y, START_X] = [-1, -1]
        cost_maps[START_Y, START_X] = 0
        q = heapdict()
        q[START_Y * W + START_X] = 0
        goal = settle_list[0]

        while len(q) > 0:
            current = q.popitem()
            h = np.int32(current[0] / W)
            w = np.int32(current[0] % W)
            searched_maps[h, w] = 1

            if w == goal[0] and h == goal[1]:
                route = [[w, h]]
                pointer = [w, h]
                while np.all(precursor_maps[pointer[1], pointer[0]] != [-1, -1]):
                    route.append(precursor_maps[pointer[1], pointer[0]].tolist())
                    pointer = precursor_maps[pointer[1], pointer[0]].tolist()
                result[goal[1] * W + goal[0]] = list(reversed(route))
                # cost[goal[1] * W + goal[0]] = cost_maps[goal[1], goal[0]]
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
                if is_legal(maps, neighbor_hor_ver[i], W, H) and searched_maps[
                    neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]] == 0:
                    height_diff = np.abs(
                        height(maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]]) - height(maps[h, w]))
                    if height_diff <= MAX_ROCK_HEIGHT:
                        appr_cost = np.abs(np.abs(neighbor_hor_ver[i][1] - goal[1]) - np.abs(
                            neighbor_hor_ver[i][0] - goal[0])) * 10 + min(np.abs(neighbor_hor_ver[i][1] - goal[1]),
                                                                          np.abs(neighbor_hor_ver[i][0] - goal[0])) * 14
                        new_cost = cost_maps[h, w] + 10 + muddiness(
                            maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]]) + height_diff
                        if new_cost < cost_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]]:
                            precursor_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]] = [w, h]
                            cost_maps[neighbor_hor_ver[i][1], neighbor_hor_ver[i][0]] = new_cost
                            q[neighbor_hor_ver[i][1] * W + neighbor_hor_ver[i][0]] = new_cost + appr_cost

            for i in range(4):
                if is_legal(maps, neighbor_dia[i], W, H) and searched_maps[neighbor_dia[i][1], neighbor_dia[i][0]] == 0:
                    height_diff = np.abs(height(maps[neighbor_dia[i][1], neighbor_dia[i][0]]) - height(maps[h, w]))
                    if height_diff <= MAX_ROCK_HEIGHT:
                        appr_cost = np.abs(
                            np.abs(neighbor_dia[i][1] - goal[1]) - np.abs(neighbor_dia[i][0] - goal[0])) * 10 + min(
                            np.abs(neighbor_dia[i][1] - goal[1]), np.abs(neighbor_dia[i][0] - goal[0])) * 14
                        new_cost = cost_maps[h, w] + 14 + muddiness(
                            maps[neighbor_dia[i][1], neighbor_dia[i][0]]) + height_diff
                        if new_cost < cost_maps[neighbor_dia[i][1], neighbor_dia[i][0]]:
                            precursor_maps[neighbor_dia[i][1], neighbor_dia[i][0]] = [w, h]
                            cost_maps[neighbor_dia[i][1], neighbor_dia[i][0]] = new_cost
                            q[neighbor_dia[i][1] * W + neighbor_dia[i][0]] = new_cost + appr_cost
            searched_maps[h, w] = 1
        settle_list.remove(goal)

    return result