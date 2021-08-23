from knowledge_base import Disjunction, KnowledgeBase, AtomicSentence
from utils import read_input, sentence_to_disjunction, unify, forward, forward_query, resolve
import copy
import time


def main():
    inuput_file_name = 'test_case/test_case_3.txt'
    output_file_name = 'output.txt'
    output_file = open(output_file_name, 'w')
    number_of_query, query_sentence_list, number_of_sentence, sentence_list = read_input(inuput_file_name)
    kb = KnowledgeBase()
    for i in range(number_of_sentence):
        # sentence_to_cnf(sentence_list[i]).print_sentence()
        kb.tell(sentence_to_disjunction(sentence_list[i]))
    kb.standarize_var()
    result_list = []
    for i in range(number_of_query):
        query = sentence_to_disjunction(query_sentence_list[i])
        result = resolve(copy.deepcopy(kb), sentence_to_disjunction(query_sentence_list[i]))
        print(result)
        if result:
            output_file.write('TRUE')
        else:
            output_file.write('FALSE')
        output_file.write('\n')
    output_file.close()


if __name__ == '__main__':
    main()