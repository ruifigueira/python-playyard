def inc(a):
    return a + 1

def dec(a):
    return a - 1

def is_zero(a):
    return a == 0

def cons(first, second):
    return lambda pair: pair(first, second)

def car(c):
    return c(lambda first, second: first)

def cdr(c):
    return c(lambda first, second: second)

def nil():
    return None

def is_nil(o):
    return o == None

def identity(i):
    return i

''' ----------------- '''
''' Number operations '''
''' ----------------- '''

def sig_aux(a, b):
    if is_zero(a):
        return 1
    if is_zero(b):
        return -1
    return sig_aux(dec(a), inc(b))

def sig(a):
    if is_zero(a):
        return 0
    return sig_aux(a, a)

def is_pos(a):
    if is_zero(a):
        return False
    return is_zero(dec(sig(a)))

def neg_aux(a, b):
    if is_zero(a):
        return b
    if is_pos(a):
        return neg_aux(dec(a), dec(b))
    return neg_aux(inc(a), inc(b))

def neg(a):
    return neg_aux(a, 0)

def is_neg(a):
    if is_zero(a):
        return False
    return is_pos(neg(a))

def sum(a, b):
    if is_zero(a):
        return b
    if is_pos(a):
        return sum(dec(a), inc(b))
    return sum(inc(a), dec(b))

def sub(a, b):
    return sum(a, neg(b))

def is_equal(a, b):
    return is_zero(sub(a, b))

def is_great(a, b):
    return is_pos(sub(a, b))

def is_less(a, b):
    return is_neg(sub(a, b))

def mult(a, b):
    if is_zero(b):
        return 0
    if is_pos(b):
        return sum(a, mult(a, dec(b)))
    return neg(mult(a, neg(b)))

def div_aux(a, b):
    if is_zero(a):
        return 0
    if is_neg(a):
        return -1
    return inc(div_aux(sub(a, b), b))

def div(a, b):
    if is_neg(a):
        return neg(div(neg(a), b))
    if is_neg(b):
        return neg(div(a, neg(b)))
    return div_aux(a, b)

def mod(a, b):
    if is_neg(a):
        return neg(mod(neg(a), b))
    if is_neg(a):
        return mod(a, neg(b))
    if is_pos(sub(a, b)):
        return mod(sub(a, b), b)
    return a

''' --------------- '''
''' List operations '''
''' --------------- '''

def foldl(lst, fn, accum):
    if is_nil(lst):
        return accum
    return foldl(cdr(lst), fn, fn(accum, car(lst)))

def foldr(lst, fn, accum):
    if is_nil(lst):
        return accum
    return fn(car(lst), foldr(cdr(lst), fn, accum))

def foldl_with_index(lst, fn, accum):
    return cdr(foldl(lst, lambda c, v: cons(inc(car(c)), fn(cdr(c), v, car(c))), cons(0, accum)))

def nth(lst, i):
    return foldl_with_index(lst, lambda a, v, idx: v if is_equal(idx, i) else a, nil())

def first(lst):
    return nth(lst, 0)

def size(lst):
    return foldl(lst, lambda x, y: inc(x), 0)

def reverse(lst):
    return foldr(lst, cons, nil())

def map(lst, fn):
    return foldl(lst, lambda a, b: cons(fn(a), b), nil())

def filter(lst, fn):
    if is_nil(lst):
        return nil()
    if fn(car(lst)):
        return cons(car(lst), filter(cdr(lst), fn))

