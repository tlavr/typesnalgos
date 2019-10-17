from stack import *

def bracketparser(line):
    stack = Stack()
    for i in line:
        if i == ')':
            if stack.pop() is None:
                print('Parentheses are not balanced!')
                return False
        elif i == '(':
            stack.push(i)
    if stack.size() > 0:
        print('Parentheses are not balanced!')
        return False
    print('Parentheses are balanced!')
    return True

def postcalc(line):
    line = ''.join(line.split())
    stack1 = StackFIFO()
    stack2 = Stack()
    for i in line:
        stack1.push(i)
    while stack1.size()>0:
        ch = stack1.pop()
        print(ch)
        if ch == '+':
            stack2.push(stack2.pop()+stack2.pop())
        elif ch == '*':
            stack2.push(stack2.pop() * stack2.pop())
        elif ch == '=':
            return stack2.peek()
        else:
            stack2.push(int(ch))


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

""" # brackets test
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

""" #calc test
exp1 = '1 2 + 3 * =' #(1+2)*3=
exp2 = '8 2 + 5 * 9 + =' # (8+2)*5 + 9 =
exp3 = '45+3*3+4*=' # ((4+5)*3 + 3)*4
print(postcalc(exp1)) #9
print(postcalc(exp2)) #59
print(postcalc(exp3)) #120
# """

