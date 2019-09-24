#!/usr/bin/env python3

import fileinput as fi

OPERATOR_NOT        = 'n'
OPERATOR_AND        = 'c'
OPERATOR_OR         = 'd'
OPERATOR_IMPLIES    = 'i'
OPERATORS           = [OPERATOR_NOT, OPERATOR_AND, OPERATOR_OR, OPERATOR_IMPLIES]
OPERATORS_N         = [OPERATOR_AND, OPERATOR_OR, OPERATOR_IMPLIES]

def substring(string, fromm, howmany):
    return string[fromm:fromm+howmany]

def fully_braced(f):
    if len(f) == 1 and str.isupper(f[0]):
        return True

    elif len(f) >= 1 and OPERATOR_NOT in f[0]:
        return fully_braced(f[1:])

    else:
        brackets = 0
        op_pos = 0

        for i, c in enumerate(f, start=0):
            if c == '(':
                brackets += 1

            elif c == ')':
                brackets -= 1

            elif brackets == 1 and c in OPERATORS_N:
                op_pos = i

        if op_pos == 0:
            return False

        left = substring(f, 1, op_pos-1)
        right = substring(f, op_pos+1, len(f)-op_pos-2);

        return brackets == 0 and fully_braced(left) and fully_braced(right)

class Formula():
    operator = ''
    right = None
    left = None

    def __str__(self):
        return self.operator

    def __init__(self, f):
        if len(f) == 1:
            self.operator = f[0]

        elif f[0] == OPERATOR_NOT:
            self.operator = OPERATOR_NOT
            self.right = Formula(f[1:])

        else:
            brackets = 0

            for i, c in enumerate(f, start=0):
                if c == '(':
                    brackets += 1

                elif c == ')':
                    brackets -= 1

                elif brackets == 1 and (c in OPERATORS_N):
                    self.operator = c
                    self.left = Formula(substring(f, 1, i-1))
                    self.right = Formula(substring(f, i+1, len(f)-i-2))

    def stree(self, depth = 0):
        if self.right:
            self.right.stree(depth + 1)

        print(depth * "---", self.operator, '(' + str(depth) + ')')

        if self.left:
            self.left.stree(depth + 1)

    def inorder(self):
        if str.isupper(self.operator):
            return self.operator

        elif self.operator == OPERATOR_NOT:
            return OPERATOR_NOT + self.right.inorder()

        else:
            ret = "("

            if self.left:
                ret += self.left.inorder()

            ret += self.operator

            if self.right:
                ret += self.right.inorder()

            ret += ")"

            return ret

    def inorder_minimize(self, bracket_needed = False):
        if str.isupper(self.operator):
            return self.operator

        elif self.operator == OPERATOR_NOT:
            return OPERATOR_NOT + self.right.inorder_minimize()

        else:
            left_str = ''
            right_str = ''

            if self.left:
                if ((self.left.operator == self.operator and self.operator != OPERATOR_IMPLIES)                     or (self.operator == OPERATOR_IMPLIES and self.left.operator in [OPERATOR_AND, OPERATOR_OR])):
                    left_str = self.left.inorder_minimize()
                else:
                    left_str = self.left.inorder_minimize(True)

            if self.right:
                if ((self.right.operator == self.operator and self.operator != OPERATOR_IMPLIES)                     or (self.operator == OPERATOR_IMPLIES and self.right.operator in [OPERATOR_AND, OPERATOR_OR])):
                    right_str = self.right.inorder_minimize()
                else:
                    right_str = self.right.inorder_minimize(True)


        leftb = "(" if bracket_needed else ""
        rightb = ")" if bracket_needed else ""
        return leftb + left_str + self.operator + right_str + rightb


    def subformulas(self):
        subformulas = {self.inorder()}

        if self.right:
            self.right.gather_subformulas(subformulas)

        if self.left:
            self.left.gather_subformulas(subformulas)

        return subformulas

    def gather_subformulas(self, sf):
        sf.add(self.inorder())

        if self.right:
            self.right.gather_subformulas(sf)

        if self.left:
            self.left.gather_subformulas(sf)

    def complexity(self):
        # atomi formuláé 0
        if str.isupper(self.operator):
            return 0

        sum = 1

        if self.right:
            sum += self.right.complexity()

        if self.left:
            sum += self.left.complexity()

        return sum

    def tex(self):
        texops = {
                OPERATOR_IMPLIES: '$\supset$',
                OPERATOR_NOT: '$\lnot$',
                OPERATOR_OR: '$\lor$',
                OPERATOR_AND: '$\land$'
                }


        ret = r'''['''
        ret += texops[self.operator] if self.operator in OPERATORS else '$' + self.operator + '$'

        if self.left:
            ret += self.left.tex()

        if self.right:
            ret += self.right.tex()

        ret += r''']'''
        return ret

if __name__ == '__main__':
    for formula in fi.input():
        formula = formula.strip('\n')

        print('> kapott formula:', formula)
        print('> fully_braced?', fully_braced(formula))

        if fully_braced(formula):
            f = Formula(formula)
            print('> szerkezeti fa:')
            f.stree()
            print('> inorder:', f.inorder())
            print('> zárójel elhagyással:', f.inorder_minimize())
            print('> részformulák halmaza:')
            for s in f.subformulas():
                print('\t -', s)
            print('logikai összetettség:', f.complexity())
            print('tex:')
            print(f.tex())

        print('-------------------------------------------')


