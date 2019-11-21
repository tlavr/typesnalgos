from bloomfilt import *

bf = BloomFilter(32)

def cycshift(str1):
    l = len(str1)
    return str1[1:len(str1)] + str1[0]

test_str = "0123456789"
bf.add(cycshift(test_str))


for i in range(len(test_str)):
    print(test_str)
    print(bin(bf.hash1(test_str)))
    print(bin(bf.hash2(test_str)))
    print(bin(bf.filter))
    print(bf.is_value(test_str))
    test_str = cycshift(test_str)
