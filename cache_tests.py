from cache import *

def print_cache(cache):
    for ii in range(cache.size):
        print('Cache idx: '+str(ii)+' value: '+str(cache.slots[ii])+' hits: '+str(cache.hits[ii])+'\n')
    print('\n')

cache_size = 10
cache = NativeCache(cache_size)
for ii in range(cache_size):
    cache.put(ii)
print_cache(cache)

for jj in range(5):
    for ii in range(cache_size):
        if ii != 1 and ii != 3:
            cache.find(ii)
print_cache(cache)

cache.put(99)
cache.find(99)
cache.put(99)

print_cache(cache)