#! /usr/bin/env python

import os
import sys
from copy import deepcopy

DEBUG = False
ops = "&|-><="

#class cnf tree node
class cnf_node:
    def __init__(self,lemon):
        self.symbol = lemon
        self.left = None
        self.right = None
        self.neg = False

    def compliment(self):
        self.neg = 1 - self.neg

    def set_child(self,choco=None,cake=None):
        self.left, self.right = choco, cake

    def set_symbol(self,sugar):
        self.symbol = sugar

    def __deepcopy__(self,_):
        left, right = None, None
        if self.symbol in ops:
            left = deepcopy(self.left)
            right = deepcopy(self.right)
        copy = cnf_node(self.symbol)
        copy.set_child(left,right)
        if self.neg:
            copy.compliment()
        return copy

    def __str__(self):
        return ('- ' if self.neg else '') + self.symbol
    def __repr__(self):
        return ('- ' if self.neg else '') + self.symbol

def gen_tree(np):
    def pop_op(sym):
        if sym in "&|><=":
            return (stack.pop(),stack.pop())
        elif sym == '-':
            stack[-1].compliment()
        else:
            return (None,None)

    stack = []
    for sym in np[::-1]:
        if sym == '-':
            stack[-1].compliment()
        else:
            node = cnf_node(sym)
            if sym in "&|><=":
                node.set_child(stack.pop(),stack.pop())
            stack.append(node)
    return node

#a->b : a'+b
#a=b : (a->b)(b->a) : (a'+b)(a+b') : a'a+a'b'+ab+bb' : ab+a'b'
def impl_eq_free(cur):
    if not cur.symbol in "&|><=": return
    if cur.symbol == '=':
        left = cnf_node('|')
        right = cnf_node('|')
        left.set_child(deepcopy(cur.left),deepcopy(cur.right))
        left.left.compliment()
        right.set_child(deepcopy(cur.left),deepcopy(cur.right))
        right.right.compliment()
        cur.set_symbol('&')
        cur.set_child(left,right)
    elif cur.symbol == '>':
        cur.left.compliment()
        cur.set_symbol('|')
    elif cur.symbol == '<':
        cur.right.compliment()
        cur.set_symbol('|')
    impl_eq_free(cur.left)
    impl_eq_free(cur.right)

def nnf(cur):
    if not cur.symbol in "&|": return
    if cur.neg:
        cur.compliment()
        cur.left.compliment()
        cur.right.compliment()
        if cur.symbol == '&':
            cur.set_symbol('|')
        elif cur.symbol == '|':
            cur.set_symbol('&')
    nnf(cur.left)
    nnf(cur.right)

def cnf(cur):
    if not cur.symbol in "&|": return
    cnf(cur.left)
    cnf(cur.right)
    if cur.symbol == '|':
        if cur.left.symbol != '&':
            cur.set_child(cur.right,cur.left)
        if cur.left.symbol == '&':
            left = cnf_node('|')
            right = cnf_node('|')
            cur.set_symbol('&')
            left.set_child(cur.right,cur.left.left)
            right.set_child(cur.right,cur.left.right) # not need deepcopy
            cur.set_child(left,right)
            cnf(cur.left)
            cnf(cur.right)


#function generating cnf tree
#return root cnf_node of tree
#this function doesn't check invalid syntax of propositional formula
def gen_cnf_tree(np):
    root = gen_tree(np)
    print prefix_res(root)
    impl_eq_free(root)
    print prefix_res(root)
    nnf(root)
    print prefix_res(root)
    cnf(root)
    return root

def prefix_res(cur):
    if not cur: return ''
    res = ('- %s %s %s' if cur.neg else '%s %s %s')%(cur.symbol,prefix_res(cur.left),prefix_res(cur.right))
    return res

def infix_res(cur):
    if not cur: return ''
    res = ('(%s) ' if cur.symbol=='&' and cur.left.symbol=='|' else '%s ')%infix_res(cur.left)\
            + ('- %s ' if cur.neg else '%s ')%cur.symbol\
            + ('(%s)' if cur.symbol=='&' and cur.right.symbol=='|' else '%s')%infix_res(cur.right)
    return res

def validity(infix):
    clauses = infix.split(' & ')
    for clause in clauses:
        clause = clause.replace(' ','')
        if clause[0]!='(': return False
        clause = clause[1:-1].split('|')
        lits = {}
        for lit in clause:
            if lit[0]=='-':
                fire = False
                lit = lit[1:]
            else:
                fire = True
            if not lits.get(lit):
                lits[lit] = fire
            elif lits[lit] != fire:
                break
        else:
            return False
    return True


if __name__ == '__main__':
    if DEBUG:
        np = '> & - p q & p > r q'
    else:
        np = sys.argv[1]

    root = gen_cnf_tree(np.split())
    print ' '.join(prefix_res(root).split())
    infix = ' '.join(infix_res(root).split())
    print infix
    print 'Valid' if validity(infix) else 'Not Valid'

