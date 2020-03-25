import numpy as np

#1.A
M = np.arange(2, 27)
print(M)
print("")

#1.B
M = M.reshape(5,5)
print(M)
print("")

#1.C
M[1:4, 1:4] = 0
print(M)
print("")

#1.D
M = M @ M
print(M)
print("")

#1.E
v = M[0]
ans = np.sqrt((v @ v))
print(ans)
