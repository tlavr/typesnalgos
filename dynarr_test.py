from dynarrays import *
N = 32

da = DynArray()
da.print_arr()

for i in range(N):
    da.insert(0,i)
da.print_arr()
#da.insert(13,120)

for i in range(1+int(N/2)):
    da.delete(0)
da.print_arr()