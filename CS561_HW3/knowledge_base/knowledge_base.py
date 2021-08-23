import numpy as np
# from utils import sentence_to_cnf
import utils
from .disjunction import Disjunction
from utils import unify
import copy


class KnowledgeBase:
    """
    知识库 类
    """
    def __init__(self):
        self.knowledge_base = {}

    # 将新的析取式加入知识库
    def tell(self, disjunction):
        # 获取 disjunction 的谓词集合
        predicate_list = disjunction.get_predicate()

        # 用于返回新加入的位置索引
        position_list = []

        # 将 disjunction 加入字典，并记录其在字典中的位置索引
        for predicate in predicate_list:
            if predicate in self.knowledge_base.keys():
                length = len(self.knowledge_base[predicate])
                self.knowledge_base[predicate].append(disjunction)
                position_list.append([predicate, length])
            else:
                self.knowledge_base[predicate] = [disjunction]
                position_list.append([predicate, 0])
        return position_list

    # 获取 知识库的 谓词集合 列表形式
    def get_predicate(self):
        predicate_list = []
        for _, disjunction_list in self.knowledge_base.items():
            for disjunction in disjunction_list:
                if disjunction is None:
                    continue
                predicate_list += disjunction.get_predicate()
        return list(set(predicate_list))

    # 标准化 变量
    def standarize_var(self):
        var_set = set()
        for predicate, disjunction_list in self.knowledge_base.items():
            for disjunction in disjunction_list:
                if disjunction.standarize_flag is True:
                    continue
                else:
                    tmp_var_set = disjunction.get_var_set()
                    for var_name in tmp_var_set:
                        if var_name in var_set:
                            new_name = var_name
                            i = 0
                            while new_name in var_set:
                                new_name = var_name[0] + str(i)
                                i += 1
                            disjunction.update_var_name(var_name, new_name)
                            var_set.add(new_name)
                        else:
                            var_set.add(var_name)
                    disjunction.set_standarize_flag()

    # 检查 新的disjunctiion 是否已经在知识库中
    # 可优化
    def check_repeat(self, new_disjunction):
        predicate_check = new_disjunction.get_predicate()[0]
        disjunction_list = self.knowledge_base[predicate_check]
        for disjunction in disjunction_list:
            if new_disjunction.is_repeat(disjunction):
                return True
        return False

    # 检查 新的disjunctiion 是否已经被包含知识库中
    def check_entail(self, new_disjunction):
        predicate_check_list = new_disjunction.get_predicate()
        for predicate_check in predicate_check_list:
            disjunction_list = self.knowledge_base[predicate_check]
            for disjunction in disjunction_list:
                if new_disjunction.is_entail(disjunction): # disjunction 可以 推出 new_disjunction 小可以推出大
                    return True
            return False

    # 计算当前 知识库 中含有多少条语句 使用了 count 标记位
    def get_size(self):
        count = 0
        for predicate, disjunction_list in self.knowledge_base.items():
            for disjunction in disjunction_list:
                disjunction.count_flag = False
        for predicate, disjunction_list in self.knowledge_base.items():
            for disjunction in disjunction_list:
                if disjunction.count_flag is False:
                    count += 1
                    disjunction.count_flag = True
        return count

    # 展示
    def print_predicate(self):
        print(self.knowledge_base.keys())

    def print_all(self):
        for predicate, disjunction_list in self.knowledge_base.items():
            for disjunction in disjunction_list:
                disjunction.print_flag = False
        for predicate, disjunction_list in self.knowledge_base.items():
            for disjunction in disjunction_list:
                if disjunction.print_flag is False:
                    disjunction.print_sentence()
                    disjunction.print_flag = True

#    def add_used(self, predicate, index_1, index_2, atom_index_1, atom_index_2):
#     if predicate not in self.used.keys():
#         self.used[predicate] = [[index_1, index_2, atom_index_1, atom_index_2]]
#         self.disjunction_used[predicate] = [[index_1, index_2]]
#     else:
#         self.used[predicate].append([index_1, index_2, atom_index_1, atom_index_2])
#         self.disjunction_used[predicate].append([index_1, index_2])

#     def remove(self, disjunction):
#     predicate_list = disjunction.get_predicate()
#     for predicate in predicate_list:
#         index_list = disjunction.position[predicate]
#         for index in index_list:
#             self.knowledge_base[predicate][index] = None
#         if set(self.knowledge_base[predicate]) == {None}:
#             del (self.knowledge_base[predicate])
#     # in_kb_position = disjunction.position[predicate][index]
#     # self.knowledge_base[predicate][in_kb_position] = None
#     # if set(self.knowledge_base[predicate]) == {None}:
#     #     del(self.knowledge_base[predicate])
#     # disjunction.position[predicate][index] = None
#     # disjunction.atomic_sentence_dict[predicate][index] = None
#     # if set(disjunction.atomic_sentence_dict[predicate]) == {None}:
#     #     del(disjunction.atomic_sentence_dict[predicate])
#     #     del(disjunction.position[predicate])
