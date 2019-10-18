from stack import *

# stack test
s = Stack()
N = 5
for i in range(N):
    s.push(i)
    print('size: ', s.size())

for i in range(N):
    print('value: ', s.pop())
    print('peek: ', s.peek())
    print('size: ', s.size())

while s.size() > 0:
    print(s.pop())
    print(s.pop())
# """

# brackets test
#balanced
br1 = '(((()(())((())))))'
br2 = '()'
br3 = '(()()())'

#unbalanced
ub1 = '(()'
ub2 = '('
ub3 = ')'
ub4 = '(((((()()()()))))))'
ub5 = '((((((()()()())))))'

bracketparser(br1)
bracketparser(br2)
bracketparser(br3)

bracketparser(ub1)
bracketparser(ub2)
bracketparser(ub3)
bracketparser(ub4)
bracketparser(ub5)
#"""

#calc test
exp1 = '1 2 + 3 * =' #(1+2)*3=
exp2 = '8 2 + 5 * 9 + =' # (8+2)*5 + 9 =
exp3 = '45+3*3+4*=' # ((4+5)*3 + 3)*4
print(postcalc(exp1)) #9
print(postcalc(exp2)) #59
print(postcalc(exp3)) #120
# """

