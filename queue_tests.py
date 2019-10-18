from queues import *

qu = QueueStack()
N = 15
for i in range(N):
    qu.enqueue(i)
"""
while qu.size() > 0:
    print(qu.dequeue())
"""

#qu.cycleshift(0)

while qu.size() > 0:
    print(qu.dequeue())

qu.enqueue(5)
qu.enqueue(6)
print(qu.dequeue())
print(qu.dequeue())
print(qu.dequeue())