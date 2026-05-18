import numpy as np
import matplotlib.pyplot as plt
N = 4
grid = np.zeros(N*N).reshape(N,N)
x = np.random.choice([0,255],4*4,p=[0.1,0.9]).reshape(4,4)
plt.imshow(x,interpolation='nearest')
plt.show()