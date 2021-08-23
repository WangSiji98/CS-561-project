from .unify import unify
from .sentence_to_disjuntion import sentence_to_disjunction
import queue
import time


# 前向链接，推到出知识库中所有能够推导的东西
def forward(kb):
    # 未处理队列
    unprocessed = queue.Queue()

    # 已处理列表
    processed = []

    # 将知识库中已有的 析取式 根据其谓词 入栈
    for predicate, disjunction_list in kb.knowledge_base.items():
        for i in range(len(disjunction_list)):
            unprocessed.put([predicate, i])

    num = 0

    # 循环终止条件 队列中为空
    while not unprocessed.empty():
        # print(num)
        # num += 1
        # print(unprocessed.qsize())
        start_time = time.time()
        # 获取栈顶元素
        predicate, index = unprocessed.get()

        # 检查是否已处理
        if [predicate, index] in processed:
            continue
        else:
            processed.append([predicate, index])

        # 每一个disjunction仅和index位于其之前的disjunction进行归结
        if index == 0:
            continue
        else:
            for index_before in range(index - 1):
                disjunction_1 = kb.knowledge_base[predicate][index_before]
                disjunction_2 = kb.knowledge_base[predicate][index]
                # if disjunction_1.get_size() > 2 or disjunction_2.get_size() > 2:
                #     continue
                result_list = unify(kb, disjunction_1, disjunction_2, predicate)
                for item in result_list:
                    empty_flag = item[0]
                    new_list = item[1]
                    if empty_flag is True:
                        continue
                    else:
                        if new_list:
                            for new in new_list:
                                unprocessed.put(new)
                            # 打印
                            print('resolve <'+ predicate + '>:')
                            print(index_before)
                            kb.knowledge_base[predicate][index_before].print_sentence()
                            print(index)
                            kb.knowledge_base[predicate][index].print_sentence()
                            print('=>')
                            a = new_list[0]
                            kb.knowledge_base[a[0]][a[1]].print_sentence()
                            print('\n')

        end_time = time.time()
        # print(end_time - start_time)


# 将query的否定加入知识库，并查询是否能归结出空子句
def forward_query(kb, query):
    query_negation = query.negate()
    query_position_list = kb.tell(query_negation)
    unprocessed = queue.Queue()

    for item in query_position_list:
        unprocessed.put(item)

    while not unprocessed.empty():
        predicate, index = unprocessed.get()

        if index == 0:
            continue
        else:
            for index_before in range(index - 1):
                result_list = unify(kb, kb.knowledge_base[predicate][index_before], kb.knowledge_base[predicate][index], predicate)
                for item in result_list:
                    empty_flag = item[0]
                    new_list = item[1]
                    if empty_flag is True:
                        return True
                    else:
                        for new in new_list:
                            unprocessed.put(new)
    return False



