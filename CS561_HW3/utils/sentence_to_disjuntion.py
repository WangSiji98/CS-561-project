from knowledge_base import AtomicSentence
import re
from knowledge_base import Disjunction


# 将 sentence 转化为 cnf 的 disjunction 形式
def sentence_to_disjunction(sentence):
    item_list = sentence.split(' ')
    result_list = []

    if '=>' not in item_list:
        negation_flag = False
        item = item_list[0]
        result_list.append(analyse(item, negation_flag))

    else:
        inference_position = item_list.index('=>')
        for i in range(inference_position):
            negation_flag = True
            item = item_list[i]
            if item == '&':
                continue
            result_list.append(analyse(item, negation_flag))
        negation_flag = False
        item = item_list[-1]
        result_list.append(analyse(item, negation_flag))

    return Disjunction(result_list)


# 分析 句子中的每一个原子句，返回 原子句 的形式
def analyse(item, negation_flag):
    parenthesis_position = re.search('(\(.*\))', item)

    if parenthesis_position is None:
        if item[0] == '~' and not negation_flag:
            return AtomicSentence(None, item[1:], 0)
        elif item[0] != '~' and negation_flag:
            return AtomicSentence(None, item, 0)
        elif item[0] == '~' and negation_flag:
            return AtomicSentence(None, item[1:], 1)
        elif item[0] != '~' and not negation_flag:
            return AtomicSentence(None, item, 1)
    else:
        left_parenthesis, right_parenthesis = parenthesis_position.span()
        argument_list = item[left_parenthesis + 1:right_parenthesis - 1].split(',')
        if item[0] == '~' and not negation_flag:
            return AtomicSentence(item[1:left_parenthesis], argument_list, 0)
        elif item[0] != '~' and negation_flag:
            return AtomicSentence(item[:left_parenthesis], argument_list, 0)
        elif item[0] == '~' and negation_flag:
            return AtomicSentence(item[1:left_parenthesis], argument_list, 1)
        elif item[0] != '~' and not negation_flag:
            return AtomicSentence(item[:left_parenthesis], argument_list, 1)