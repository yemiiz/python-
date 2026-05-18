#实现康威生命游戏
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys,argparse

def random_grid(N):
    """returns a grid of NxN random values"""
    return np.random.choice([255, 0], N*N, p=[0.2, 0.8]).reshape(N, N)

def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 255, 0],
                       [0, 0, 255],
                       [255, 255, 255]])
    grid[i:i+3, j:j+3] = glider