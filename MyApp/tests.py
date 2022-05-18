import numpy as np
from numpy import arange, asarray
import PIL




# a = arange(1, 25).reshape(2, 4, 3)
# r = a[:, :, 0]
# g = a[:, :, 1]
# b = a[:, :, 2]
# print(r)
# print(g)
# print(b)
# x = np.zeros((r.shape[0], r.shape[1], 3), dtype=int)
# x[:, :, 0] = r
# x[:, :, 1] = g
# x[:, :, 2] = b
# print(np.array_equal((r.flatten() + g.flatten() + b.flatten()).reshape(a.shape[0],a.shape[1], a.shape[2]), a))