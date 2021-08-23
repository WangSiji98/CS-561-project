import copy


class Disjunction:
    """
    析取式 类
    """
    def __init__(self, target_list):
        self.atomic_sentence_dict = {}
        # 标志位 用作不同的遍历功能
        self.standarize_flag = False
        self.print_flag = False
        self.count_flag = False

        # 用于削减 target_list 中的重复项
        atomic_sentence_list = []
        for i in range(len(target_list)):
            flag = True
            for j in range(i+1, len(target_list), 1):
                if target_list[i].is_equal(target_list[j]):
                    flag = False
                    break
            if flag:
                atomic_sentence_list.append(target_list[i])

        self.length = len(atomic_sentence_list)

        # 加入 hash 字典并记录 谓词
        self.predicate_list = []
        for item in atomic_sentence_list:
            predicate = item.get_predicate()
            if predicate in self.atomic_sentence_dict:
                self.atomic_sentence_dict[predicate].append(item)
            else:
                self.atomic_sentence_dict[predicate] = [item]
            self.predicate_list.append(predicate)

        # 获取变量集合
        self.var_set = set()
        for item in atomic_sentence_list:
            for arg in item.get_argument():
                if arg[0].islower():
                    self.var_set.add(arg)

    # 获取子句数量
    def get_size(self):
        return self.length

    # 将 standarize 标志位反转
    def set_standarize_flag(self):
        self.standarize_flag = True

    # 获取变量集合
    def get_var_set(self):
        return self.var_set

    # 获取 谓词集合
    def get_predicate(self):
        return list(set(self.predicate_list))

    # 生成 原子子句 列表 引用传递
    def generate_atomic_sentence_list(self):
        atomic_sentence_list = []
        for key, value in self.atomic_sentence_dict.items():
            atomic_sentence_list += value
        return atomic_sentence_list

    # 更新变量名称 用于 标准化
    def update_var_name(self, var, new_var_name):
        for predicate in self.predicate_list:
            atomic_sentence_list = self.atomic_sentence_dict[predicate]
            for atomic_sentence in atomic_sentence_list:
                atomic_sentence.update_var_name(var, new_var_name)
        self.var_set.remove(var)
        self.var_set.add(new_var_name)

    # 变量赋值 用于 合一
    def assign_var(self, var, new_var_name):
        for predicate in self.predicate_list:
            atomic_sentence_list = self.atomic_sentence_dict[predicate]
            for atomic_sentence in atomic_sentence_list:
                atomic_sentence.update_var_name(var, new_var_name)
        self.var_set.remove(var)
        self.var_set.add(new_var_name)

    # 取反
    def negate(self):
        for _, atomic_sentence_list in self.atomic_sentence_dict.items():
            for atomic_sentence in atomic_sentence_list:
                atomic_sentence.negate()
        return self

    # 去除指定原子子句 返回剩余原子子句的列表的 拷贝 值传递
    def remove_list(self, predicate, index):
        atomic_sentence_list = []
        for key, value in self.atomic_sentence_dict.items():
            if key == predicate:
                atomic_sentence_list += value[:index]
                atomic_sentence_list += value[index+1:]
            else:
                atomic_sentence_list += value
        return copy.deepcopy(atomic_sentence_list)

    # 判断是否是永真
    def is_autology(self):
        for predicate in self.get_predicate():
            atomic_sentence_list = self.atomic_sentence_dict[predicate]
            if len(atomic_sentence_list) == 1:
                continue
            else:
                for i in range(len(atomic_sentence_list)):
                    for j in range(i+1, len(atomic_sentence_list), 1):
                        if atomic_sentence_list[i].is_negate(atomic_sentence_list[j]):
                            return True
        return False

    # 检查是否重复
    def is_repeat(self, disjunction):
        self_atom_list = self.generate_atomic_sentence_list()
        target_atom_list = disjunction.generate_atomic_sentence_list()
        if len(self_atom_list) != len(target_atom_list):
            return False
        index_used = []
        for index_1, atom_1 in enumerate(self_atom_list):
            for index_2, atom_2 in enumerate(target_atom_list):
                if atom_1.is_equal(atom_2) and index_2 not in index_used:
                    index_used.append(index_2)
                    break
        if len(index_used) != len(target_atom_list):
            return False
        else:
            return True

    # 检查是否包含
    def is_entail(self, disjunction):
        self_atom_list = self.generate_atomic_sentence_list()
        target_atom_list = disjunction.generate_atomic_sentence_list()
        if len(self_atom_list) < len(target_atom_list):
            return False
        index_used = []
        for index_1, atom_1 in enumerate(target_atom_list):
            for index_2, atom_2 in enumerate(self_atom_list):
                if atom_1.is_equal(atom_2) and index_2 not in index_used:
                    index_used.append(index_2)
                    break
        if len(index_used) != len(target_atom_list):
            return False
        else:
            return True

    # 展示
    def print_sentence(self):
        sentence = ''
        for key, value in self.atomic_sentence_dict.items():
            for disjunction in value:
                sentence += disjunction.to_sentence()
                sentence += ' | '
        sentence = sentence[0:-3]
        print(sentence)

    def print_var_set(self):
        print(self.var_set)

    def print_arg(self):
        dis_arg_list = []
        for predicate in self.predicate_list:
            atomic_sentence_list = self.atomic_sentence_dict[predicate]
            atom_arg_list = []
            for item in atomic_sentence_list:
                for arg in item.get_argument():
                    atom_arg_list.append(arg)
            dis_arg_list.append(atom_arg_list)
        print(dis_arg_list)
