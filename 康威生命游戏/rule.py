import numpy as np
N = 4
grid = np.random.choice([0,255],N*N,p=[0.1,0.9]).reshape(N,N)
for i in range(N):
    for j in range(N):
        total = int(((grid[i, (j-1)%N] + grid[i, (j+1)%N] + grid[(i-1)%N, j] + grid[(i+1)%N, j] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255))
        if grid[i,j] == 255:
            if total < 2 or total > 3:
                grid[i,j] = 0
        else:
            if total == 3:
                grid[i,j] = 255