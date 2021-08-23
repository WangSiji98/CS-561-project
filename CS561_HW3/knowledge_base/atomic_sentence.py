class AtomicSentence:
    """
    原子语句 类
    """
    def __init__(self, predicate=None, argument=[], negation=1):
        self.predicate = predicate
        self.argument = argument
        self.negation = negation

    # 获取成员
    def get_predicate(self):
        return self.predicate

    def get_argument(self):
        return self.argument

    def get_negation(self):
        return self.negation

    # 更新变量

    def update_var_name(self, var, new_var_name):
        for i in range(len(self.argument)):
            if self.argument[i] == var:
                self.argument[i] = new_var_name

    # 赋值变量
    def assign_var(self, var, new_var_name):
        for i in range(len(self.argument)):
            if self.argument[i] == var:
                self.argument[i] = new_var_name

    # 取否
    def negate(self):
        self.negation = (self.negation + 1) % 2
        return self

    # 判断是否相同
    def is_equal(self, target):
        if self.predicate == target.predicate and self.argument == target.argument and self.negation == target.negation:
            return True
        else:
            return False

    # 展示
    def print(self):
        print([self.predicate, self.argument, self.negation])

    def to_sentence(self):
        sentencce_str = ''
        if self.negation == 0:
            sentencce_str += '~'
        if self.predicate is not None:
            sentencce_str += self.predicate
            sentencce_str += '('
            for arg in self.argument:
                sentencce_str += arg
                sentencce_str += ','
            sentencce_str = sentencce_str[0:-1]
            sentencce_str += ')'
        return sentencce_str

    def is_negate(self, target):
        if self.predicate == target.predicate and self.argument == target.argument and self.negation != target.negation:
            return True
        else:
            return False
