import matplotlib.pyplot as plt
import numpy as np

y = np.loadtxt('arr_out.txt',delimiter=',')
x = np.arange(y.shape[0])

plt.plot(x,y)
plt.show()