import copy
from knowledge_base import Disjunction


# 合一 两个原子子句 返回是否能合一 以及替换表 字典形式
def unify_atomic_sentence(atomic_sentence_1, atomic_sentence_2):
    argument_list_1 = atomic_sentence_1.get_argument()
    argument_list_2 = atomic_sentence_2.get_argument()
    substitution = {}
    flag = True
    if len(argument_list_1) != len(argument_list_1):
        flag = False
        return flag, {}

    if atomic_sentence_1.get_negation() + atomic_sentence_2.get_negation() != 1:
        flag = False
        return flag, {}

    for i in range(len(argument_list_1)):
        if argument_list_1[i][0].isupper() and argument_list_2[i][0].isupper():
            if argument_list_1[i] == argument_list_2[i]:
                flag = True
                continue
            else:
                flag = False
                return flag, {}
        elif argument_list_1[i][0].islower() and argument_list_2[i][0].islower():
            if argument_list_1[i] != argument_list_2[i]:
                # flag = True
                # substitution[argument_list_1[i]] = argument_list_2[i]
                flag = False
                return flag, {}
        elif argument_list_1[i][0].islower() and argument_list_2[i][0].isupper():
            flag = True
            substitution[argument_list_1[i]] = argument_list_2[i]
        elif argument_list_1[i][0].isupper() and argument_list_2[i][0].islower():
            flag = True
            substitution[argument_list_2[i]] = argument_list_1[i]
    return flag, substitution


# 归结合一两个给定了消去项的析取式，删除互斥的原子子句，并将剩余部分合一，利用替换列表更新
def unify_disjunction(kb, disjunction_1, disjunction_2, predicate, index_1, index_2, substitution):
    # new_kb = copy.deepcopy(kb) # 需要拷贝复制一个新类，传值，每一次unify后生成的是一个全新的KB
    remove_list_1 = disjunction_1.remove_list(predicate, index_1)
    remove_list_2 = disjunction_2.remove_list(predicate, index_2)
    new_atomic_sentence_list = remove_list_1 + remove_list_2

    # for atom in new_atomic_sentence_list:
    #     print(atom.to_sentence())

    empty_flag = False

    # 对列表内的原子子句进行替换
    if not new_atomic_sentence_list:
        empty_flag = True
        return empty_flag, []
    else:
        for atomic_sentence in new_atomic_sentence_list:
            arg_list = atomic_sentence.get_argument()
            for i in range(len(arg_list)):
                if arg_list[i] in substitution.keys():
                    arg_list[i] = substitution[arg_list[i]]

        new_disjunction = Disjunction(new_atomic_sentence_list)
        if not kb.check_entail(new_disjunction) and not new_disjunction.is_autology():
            # print('\nADD')
            # new_disjunction.print_sentence()
            new_position_list = kb.tell(new_disjunction)
            # print('\n')
            return empty_flag, new_position_list
        else:
            return empty_flag, []


# 合一两个析取式 返回其所有可能的归结结果
def unify(kb, disjunction_1, disjunction_2, predicate):
    disjunction_1_candidate_list = disjunction_1.atomic_sentence_dict[predicate]
    disjunction_2_candidate_list = disjunction_2.atomic_sentence_dict[predicate]
    result_list = []
    for atom_index_1, candidate_1 in enumerate(disjunction_1_candidate_list):
        for atom_index_2, candidate_2 in enumerate(disjunction_2_candidate_list):
            # if predicate in kb.used.keys() and [index_1, index_2, atom_index_1, atom_index_2] in kb.used[predicate]:
            #     continue
            flag, substitution = unify_atomic_sentence(candidate_1, candidate_2)
            if flag:
                empty_flag, new_position_list = unify_disjunction(kb, disjunction_1, disjunction_2, predicate, atom_index_1, atom_index_2, substitution)
                result_list.append([empty_flag, new_position_list])
    return result_list


# def standardize(disjunction_1, disjunction_2):
#     """
#     standarize the variable in disjunction_1 and disjunction_2, make same name in two disjunction differernt
#
#     :param disjunction_1: Disjunction
#     :param disjunction_2: Disjunction
#     :return: Disjunction, Disjunction
#     """
#     var_set_1 = disjunction_1.get_var_set()
#     var_set_2 = disjunction_2.get_var_set()
#     var_inter_set = var_set_1.intersection(var_set_2)
#     for i, item in enumerate(var_inter_set):
#         new_var_name = item
#         while new_var_name in var_inter_set:
#             new_var_name += str(i)
#             # print(new_var_name)
#             disjunction_2.update_var_name(item, new_var_name)