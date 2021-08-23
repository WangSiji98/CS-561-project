import numpy as np
from queue import Queue
import sys
from algorithm import bfs, ucs, a_star
import os


def read_input(file_name):
    input_file = open(file_name)
    algorithm = input_file.readline()
    W, H = np.array(input_file.readline().split()).astype(np.int32)
    maps = np.zeros((H, W)).astype(np.int32)
    START_X, START_Y = np.array(input_file.readline().split()).astype(np.int32)
    MAX_ROCK_HEIGHT = np.array(input_file.readline().split()).astype(np.int32)[0]
    N = np.array(input_file.readline().split()).astype(np.int32)[0]
    settle_list = []
    for _ in range(N):
        settle_x, settle_y = np.array(input_file.readline().split()).astype(np.int32)
        settle_list.append([settle_x, settle_y])

    for line in range(H):
        maps[line, :] = np.array(input_file.readline().split())

    input_file.close()

    return algorithm, W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list

def main():
    input_file_name = 'test_case/input4.txt'
    output_file_name = 'test_case/output.txt'

    algorithm, W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list = read_input(input_file_name)
    goal_list = settle_list[:]
    output_file = open(output_file_name, 'w')
    output_file.truncate()
    # result = bfs(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list)
    # print(result)



    if algorithm == 'A*\n':
        result = a_star(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list)
    elif algorithm == 'BFS\n':
        result = bfs(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list)
    elif algorithm == 'UCS\n':
        result = ucs(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list)

    for site in goal_list:
        key = site[1] * W + site[0]
        if key in result.keys():
            # print('Yes')
            position = 1
            route = result[key]
            for point in route:
                output_file.write(str(point[0]))
                output_file.write(str(','))
                output_file.write(str(point[1]))
                if position < len(route):
                    output_file.write(' ')
                    position += 1
            # output_file.write('\n')
        else:
            print('No')
            output_file.write('FAIL')
        if site != goal_list[-1]:
            output_file.write('\n')
        # output_file.write('\n')
    output_file.close()

# def main():
#     for i in range(50):
#         input_file_name = 'TestCasesInput/input{}.txt'.format(i+1)
#         cost_list = []
#
#         algorithm, W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list = read_input(input_file_name)
#         goal_list = settle_list[:]
#
#         if algorithm == 'A*\n':
#             print('Test case {}'.format(i + 1))
#             result, cost = a_star(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list)
#             for site in goal_list:
#                 key = site[1] * W + site[0]
#                 if key in cost.keys():
#                     cost_list.append(cost[key])
#                 else:
#                     cost_list.append('FAIL')
#             print(cost_list)
#
#         if algorithm == 'UCS\n':
#             print('Test case {}'.format(i + 1))
#             result, cost = ucs(W, H, maps, START_X, START_Y, MAX_ROCK_HEIGHT, N, settle_list)
#             for site in goal_list:
#                 key = site[1] * W + site[0]
#                 if key in cost.keys():
#                     cost_list.append(cost[key])
#                 else:
#                     cost_list.append('FAIL')
#             print(cost_list)




if __name__ == '__main__':
    main()