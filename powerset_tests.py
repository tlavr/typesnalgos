from powerset import *

def printset(set):
    print('Items in the set:')
    if set is not None:
        for item in set.hash.slots:
            if item != None:
                print(item)
        print('\n')

set = PowerSet()

# put tests []
print('Put tests started!')
print('Set size is: '+str(set.size()))
try:
    printset(set)
    set.put(125)
    printset(set)
    set.put(125)
    printset(set)
    set.put('126')
    printset(set)
    set.put('125')
    printset(set)

except:
    print('Put error!')

#remove tests [125,'125','126']
print('Remove tests started!')
print('Set size is: '+str(set.size()))
try:
    set.remove(125)
    printset(set)
    set.remove(127)
    printset(set)
except:
    print('Remove error!')

#intersection tests ['125','126']
print('Intersection tests started!')
print('Set size is: '+str(set.size()))
try:
    set2 = PowerSet()
    set2.put(126)
    set2.put('128')
    set3 = PowerSet()
    set3.put(127)
    set3.put(129)
    printset(set.intersection(set2))
    printset(set.intersection(set3))
except:
    print('Intersection error!')

#union tests 1:['125','126'] 2:[126,'128'] 3: [127,129]
print('Union tests started!')
print('Set size is: '+str(set.size()))
try:
    set4 = PowerSet()
    printset(set.union(set2))
    printset(set.union(set4))
    printset(set.union(set3))
except:
    print('Union error!')

#difference tests 1:['125','126'] 2:[126,'128'] 3: [127,129] 4:[]
print('Difference tests started!')
print('Set size is: '+str(set.size()))
try:
    printset(set.difference(set4))
    printset(set.difference(set2))
    printset(set.difference(set3))
except:
    print('Difference error!')

#subset tests 1:['125','126'] 2:[126,'128'] 3: [127,129] 4:[]
print('Subset tests started!')
print('Set size is: '+str(set.size()))
try:
    set5 = PowerSet()
    set5.put('125')
    print(set.issubset(set2))
    print(set.issubset(set3))
    print(set.issubset(set4))
    print(set2.issubset(set))
    print(set.issubset(set5))
except:
    print('Subset error!')

