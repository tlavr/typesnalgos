from queues import *

qu = Queue()
N = 5
for i in range(N):
    qu.enqueue(i)
"""
while qu.size() > 0:
    print(qu.dequeue())
"""

#qu.cycleshift(2)
#cycshift(qu,2)
while qu.size() > 0:
    print(qu.dequeue())
print('------')

qu.enqueue(Node(5))
qu.enqueue(6)
print(qu.size())
print(qu.dequeue())
print(qu.dequeue())
print(qu.dequeue())
print(qu.dequeue())
print(qu.dequeue())
print(qu.size())
