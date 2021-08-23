from .unify import unify
from .sentence_to_disjuntion import sentence_to_disjunction
import queue
import time


# 直接将query的否定加入kb后进行归结
def resolve(kb, query):
    query_negation = query.negate()
    query_position_list = kb.tell(query_negation)
    # print('THE ORIGINAL KB')
    # print('the number of sentence in KB now is ' + str(kb.get_size()))
    # kb.print_all()
    # print('\n')
    # print('START RESOLVE ......')
    unprocessed = queue.LifoQueue()
    processed = []
    for predicate, disjunction_list in kb.knowledge_base.items():
        for i in range(len(disjunction_list)):
            unprocessed.put([predicate, i])

    while not unprocessed.empty():
        predicate, index = unprocessed.get()
        if [predicate, index] in processed:
            continue
        else:
            processed.append([predicate, index])
        if index == 0:
            continue
        else:
            for index_before in range(index):
                disjunction_1 = kb.knowledge_base[predicate][index_before]
                disjunction_2 = kb.knowledge_base[predicate][index]
                if disjunction_1.get_size() != 1 and disjunction_2.get_size() != 1: # 一种无脑的归结策略，仅适用于本作业
                    continue
                result_list = unify(kb, disjunction_1, disjunction_2, predicate)
                for item in result_list:
                    empty_flag = item[0]
                    new_list = item[1]
                    if empty_flag is True:
                        return True
                    else:
                        # 打印
                        if new_list:
                            # print(
                            #     '===========================================================================================================================================')
                            # print('resolve <' + predicate + '>:')
                            # print(index_before)
                            # kb.knowledge_base[predicate][index_before].print_sentence()
                            # print(index)
                            # kb.knowledge_base[predicate][index].print_sentence()
                            # print('=>')
                            # a = new_list[0]
                            # kb.knowledge_base[a[0]][a[1]].print_sentence()
                            # print('\n')
                            # print('AFTER THE STEP')
                            # print('the number of sentence in KB now is ' + str(kb.get_size()))
                            # kb.print_all()
                            # print('\n')
                            for new in new_list:
                                unprocessed.put(new)
    return False