from deque import *

def palcheck(line,needup = False):
    if ispalindrome(line,needup):
        print('Line is palindrome! :)')
    else:
        print('Line is not palindrome :(')

deq = Deque()
N = 10000
for i in range(N):
    deq.addFront(i)
while deq.size() > 0:
    print(deq.removeFront())
    print(deq.removeTail())

deq.addFront("f1")
deq.addTail("t1")
deq.addFront("f2")
deq.addTail("t2")
while deq.size() > 0:
    print(deq.removeFront())
    print(deq.size())

pal1 = 'abba'
pal2 = 'abcab'
pal3 = 'ababcbaba'
pal4 = 'Sator arepo tenet opera rotas'
pal5 = 'Но невидим архангел Мороз узором лег на храм и дивен он'
palcheck(pal1)
palcheck(pal2)
palcheck(pal3)
palcheck(pal4)
palcheck(pal4,True)
palcheck(pal5,True)

