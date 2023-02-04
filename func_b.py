import re

func_desc = ''
step = 0

def print_formula(desc: str):
    global func_desc
    global step
    _desc = desc.replace('[', '').replace(']', '')

    if desc != func_desc:
        step += 1
        print('{:<4d}'.format(step) + _desc)
        func_desc = desc


def f(n, desc = '', nest=0):
    global func_desc
    global step
    # Rule: f(n) = n+1

    print_formula(desc.format(n))
    return n + 1


def B(m: int, n: int, desc='= [B({}, {})]', nest=0):
    global func_desc
    global step


    print_formula(desc.format(m, n))


    if m == 0 and n > 0:
    # Rule1: B(0, n) = f(n)
        _desc = desc.replace('[B({}, {})]', '[f({})]')
        ans = f(n, _desc)

    elif 0 < m and n == 0:
    # Rule2: B(m, 0) = B(m-1, 1)
        _desc = desc
        ans = B(m-1, n+1, _desc, nest=nest+1)


    elif 0 < m and 0 < n:
    # Rule3: B(m, n) = B(m-1, B(m, n-1))
        desc_inner = desc.replace('[B({}, {})]', 'B({}, [B({{}}, {{}})])'.format(m-1))

        ans_inner = B(m, n-1,desc_inner, nest=nest+1)
        
        print_formula(desc.replace('[B({}, {})]','{}').format(ans))

        ans = B(m-1, ans_inner)
    
    print_formula(desc.replace('[B({}, {})]','{}').format(ans))
    return ans


def g(x):
    global func_desc
    global step

    print(' g({})'.format(x))
    # Rule: g(x) = B(x, x0)
    ans = B(x, x)

    # print('= {}'.format(ans))
    return ans




if __name__ == '__main__':
    g(3)

