import numpy as np


# 读取输入
def read_input(filename):
    input_file = open(filename)
    query_list, sentence_list = [], []

    number_of_query = int(input_file.readline().strip('\n'))
    for _ in range(number_of_query):
        query_list.append(input_file.readline().strip('\n'))

    number_of_sentence = int(input_file.readline().strip('\n'))
    for _ in range(number_of_sentence):
        sentence_list.append(input_file.readline().strip('\n'))
    input_file.close()

    return number_of_query, query_list, number_of_sentence, sentence_list
