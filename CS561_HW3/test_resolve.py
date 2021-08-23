from knowledge_base import Disjunction, KnowledgeBase, AtomicSentence
from utils import read_input, sentence_to_disjunction, unify, forward, forward_query, resolve, resolve_all
import copy
import time


def main():
    file_name = 'test_case/test_case_5.txt'
    number_of_query, query_sentence_list, number_of_sentence, sentence_list = read_input(file_name)
    kb = KnowledgeBase()
    for i in range(number_of_sentence):
        # sentence_to_cnf(sentence_list[i]).print_sentence()
        kb.tell(sentence_to_disjunction(sentence_list[i]))
    kb.standarize_var()
    # forward(kb)
    # print('\n')
    # print('the number of sentence in KB now is ' + str(kb.get_size()))
    # new_kb, result = resolve(copy.deepcopy(kb), sentence_to_disjunction(query_sentence_list[0]))
    # print('AFTER RESOLVING')
    # print('the number of sentence in KB now is ' + str(new_kb.get_size()))
    # new_kb.print_all()
    # print('\n')
    # print('the result is ')
    for i in range(number_of_query):
        query = sentence_to_disjunction(query_sentence_list[i])
        if number_of_sentence <= 10:
            print(resolve_all(copy.deepcopy(kb), sentence_to_disjunction(query_sentence_list[i])))
        else:
            print(resolve(copy.deepcopy(kb), sentence_to_disjunction(query_sentence_list[i])))
    # kb.knowledge_base['Ready'][0].print_sentence()
    # print(forward(kb, sentence_to_cnf(query_sentence_list[0])))
    # kb.knowledge_base['Ready'][0].print_sentence()

    # unify不能改变原来的


if __name__ == '__main__':
    main()