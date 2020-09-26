import numpy as np
from itertools import combinations, product, permutations, combinations_with_replacement

def generate_24p(
    lower = 1,
    upper = 9,
    num = 4,
    ans = 24,
    op_list = [np.add, np.subtract, np.multiply, np.divide],
    op_name_dict = {np.add:'+', np.subtract:'-', np.multiply:'x', np.divide:'/'},
    verbose = 1,
    error_tol = 1e-4,
):
    def is_symmetric(op):
        return True if op is np.add or op is np.multiply else False

    def calc_tree1(digit_tuple, ops):
        all_perm = list(permutations(digit_tuple))
        (op1, op2, op3) = ops 
        return [op2(op1(a, b), op3(c, d)) for a,b,c,d in all_perm]

    def calc_tree2(digit_tuple, ops):
        all_perm = list(permutations(digit_tuple))
        (op1, op2, op3) = ops 
        ret = [op3(op2(op1(a, b), c), d) for a,b,c,d in all_perm]
        if not is_symmetric(op2):
            ret+=[op3(op2(c, op1(a, b)), d) for a,b,c,d in all_perm]
            if not is_symmetric(op3):
                ret+=[op3(d, op2(c, op1(a, b))) for a,b,c,d in all_perm] + [op3(d, op2(op1(a, b), c)) for a,b,c,d in all_perm]

        else:
            if not is_symmetric(op3):
                ret+=[op3(d, op2(op1(a, b), c)) for a,b,c,d in all_perm]
        return ret

    def find_sol(digit_tuple, ops):
        """
            Here we only consider the case where len(digit_tuple)==4 and len(ops)==3
        """
        result = np.array(calc_tree1(digit_tuple, ops) + calc_tree2(digit_tuple, ops))
        for r in result:
            if abs(r-ans) < error_tol: return True 
        return False

    availables = np.arange(lower, upper+1)
    candidates = combinations_with_replacement(availables, num)
    restore = []
    for digit_tuple in candidates:
        # for a,b,c,d in permutations(digit_tuple):
        for ops in list(product(op_list, repeat=3)):
            if find_sol(digit_tuple, ops):
                restore.append(digit_tuple)
                break
    return restore
