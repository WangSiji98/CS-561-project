from utils import read_input, sentence_to_disjunction
from knowledge_base import Disjunction, KnowledgeBase, AtomicSentence
from utils import unify, unify_disjunction, unify_atomic_sentence


def test():
    file_name = 'test_case/test_case_2.txt'
    number_of_query, query_list, number_of_sentence, sentence_list = read_input(file_name)
    # analyse_term('A(x,y)', False)

    s1 = 'Healthy(x0) & Train(y,x0) => Learn(y,x0)'
    s2 = 'Ready(Ares) & Healthy(Ares) & Learn(Sit,Ares) => Graduate(Ares)'
    s3 = 'Train(y,x0) => Learn(y,x0)'
    # s3 = 'FUCK(x,y) & ~TMD(A) => SHIT(y)'
    # s1 = '~TMD(A)'
    # s2 = 'TMD(A)'
    # s3 = 'KILL(x)'
    # s4 = '~KILL(Q)'
    b1 = sentence_to_disjunction(s1)
    b2 = sentence_to_disjunction(s2)
    b3 = sentence_to_disjunction(s3)
    a1 = AtomicSentence('TMD', ['x', 'A'], 1)
    a2 = AtomicSentence('TMD', ['z', 'A'], 0)
    kb = KnowledgeBase()
    kb.tell(b1)
    kb.tell(b2)
    print(kb.check_entail(b3))
    print(b2.get_size())
    # empty_flag, new_position_list = unify_disjunction(kb, b1, b2, 'Learn', 0, 0, {'y':'sit','x0':'Ares'})
    # print(new_position_list)
    # kb.knowledge_base['Graduate'][1].print_sentence()

    # 测试 standarize_var
    # kb.knowledge_base['TMD'][0].print_sentence()
    # kb.knowledge_base['TMD'][1].print_sentence()
    # kb.standarize_var()
    # kb.knowledge_base['TMD'][0].print_sentence()
    # kb.knowledge_base['TMD'][1].print_sentence()
    # print(b2.get_var_set())


    # 测试 standarize
    # b1.print_arg()
    # b2.print_arg()
    # standardize(b1, b2)
    # b1.print_arg()
    # b2.print_arg()
    # kb.knowledge_base['DAMN'][0].print_arg()
    # standardize(b1, b2)
    # kb.knowledge_base['DAMN'][0].print_arg()

    # 测试 unify_atomic_sentence
    # flag, subsitution = unify_atomic_sentence(a1, a2)
    # print(flag)
    # print(subsitution)

    # 测试 unify_disjunction
    # a11 = b1.atomic_sentence_dict['TMD'][0]
    # a22 = b2.atomic_sentence_dict['TMD'][0]
    # flag, subsitution = unify_atomic_sentence(a11, a22)
    # empty_flag, new_list = unify_disjunction(kb, b1, b2, 'TMD', 0, 0, subsitution)
    # kb.knowledge_base['FUCK'][1].print_sentence()
    # kb.knowledge_base['DAMN'][1].print_sentence()
    # print(empty_flag)
    # print(new_list)

    # 测试 unify
    # result_list = unify(kb, b1, b2, 'TMD')
    # print(result_list)
    # kb.knowledge_base['SHIT'][1].print_sentence()

    # 测试 negate
    # aa1 = a1.negate()
    # aa1.print()

    # 测试 is_repeat
    # b1.print_sentence()
    # b3.print_sentence()
    # print(b1.is_repeat(b3))

    # 测试 check_repeat
    # print(kb.check_repeat(b3))

    # 测试 构造disjunction
    # s4 = 'FUCK(x,y) & FUCK(x,y) => SHIT(x,y)'
    # b4 = sentence_to_cnf(s4)
    # b4.print_sentence()


if __name__ == '__main__':
    test()