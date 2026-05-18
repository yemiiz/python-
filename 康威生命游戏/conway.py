import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import sys
import argparse

def random_grid(N):
    """返回一个NxN的随机网格（255=活细胞，0=死细胞）"""
    return np.random.choice([255, 0], N*N, p=[0.2, 0.8]).reshape(N, N)

def add_glider(i, j, grid):
    """添加滑翔机，左上角坐标为(i, j)"""
    glider = np.array([[0, 255, 0],
                       [0, 0, 255],
                       [255, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def addGosperGliderGun(i, j, grid):
    """修复版高斯帕滑翔机枪，无索引越界错误"""
    # 标准Gosper滑翔机枪为11行×36列，这里定义11行避免越界
    gun = np.zeros((11, 36), dtype=int)
    
    # 滑翔机枪图案（索引已修正为0~10行）
    # 左侧方块
    gun[4, 0:2] = 1
    gun[5, 0:2] = 1
    
    # 中间左侧结构
    gun[2, 12:14] = 1
    gun[3, [11, 15]] = 1
    gun[4, [10, 16]] = 1
    gun[5, [10, 14, 16, 17]] = 1
    gun[6, [10, 16]] = 1
    gun[7, [11, 15]] = 1
    gun[8, 12:14] = 1
    
    # 中间右侧结构
    gun[0, 24] = 1
    gun[1, [22, 24]] = 1
    gun[2, [20, 21]] = 1
    gun[3, [20, 21]] = 1
    gun[4, [20, 21]] = 1
    gun[5, [22, 24]] = 1
    gun[6, 24] = 1
    
    # 右侧方块
    gun[2, 34:36] = 1
    gun[3, 34:36] = 1

    # 转换为255（活细胞）并写入网格
    grid[i:i+11, j:j+36] = gun * 255

def update(frameNum, img, grid, N):
    """动画核心：逐帧更新细胞状态"""
    newGrid = grid.copy()
    # 遍历所有细胞
    for i in range(N):
        for j in range(N):
            # 计算8邻域活细胞总数（环形边界）
            total = int((
                grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
            ) / 255)

            # 康威生命游戏规则
            if grid[i, j] == 255:
                # 活细胞：<2 或 >3 个邻居 → 死亡
                if total < 2 or total > 3:
                    newGrid[i, j] = 0
            else:
                # 死细胞：=3 个邻居 → 复活
                if total == 3:
                    newGrid[i, j] = 255

    # 更新图像数据
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def main():
    """主函数：参数解析 + 网格初始化 + 动画启动"""
    # 1. 命令行参数解析
    parser = argparse.ArgumentParser(description="康威生命游戏")
    parser.add_argument('--grid-size', dest='N', required=False, type=int, default=50, help="网格大小 NxN")
    parser.add_argument('--interval', dest='interval', required=False, type=int, default=50, help="动画刷新间隔(ms)")
    parser.add_argument('--glider', action='store_true', required=False, help="启动时添加滑翔机")
    parser.add_argument('--gosper', action='store_true', required=False, help="启动时添加高斯帕滑翔机枪")
    args = parser.parse_args()

    # 2. 读取参数
    N = args.N          # 网格大小
    updateInterval = args.interval  # 刷新间隔

    # 3. 初始化游戏网格
    grid = np.array([])
    if args.glider:
        # 模式1：纯空白网格 + 单个滑翔机
        grid = np.zeros((N, N), dtype=int)
        add_glider(1, 1, grid)
    elif args.gosper:
        # 模式2：纯空白网格 + 滑翔机枪（会无限发射滑翔机）
        grid = np.zeros((N, N), dtype=int)
        addGosperGliderGun(10, 10, grid)
    else:
        # 模式3：默认随机网格
        grid = random_grid(N)

    # 4. Matplotlib 绘图 + 动画设置
    fig, ax = plt.subplots()
    ax.set_title("Conway's Game of Life")
    # 绘制初始网格（灰度图）
    img = ax.imshow(grid, interpolation='nearest', cmap='gray')

    # 5. 启动动画
    ani = animation.FuncAnimation(
        fig,                  # 画布
        update,               # 帧更新函数
        fargs=(img, grid, N), # 传递给 update 的参数
        interval=updateInterval, # 刷新间隔
        blit=True             # 优化渲染（仅重绘变化部分）
    )

    # 显示窗口
    plt.show()

# 程序入口
if __name__ == '__main__':
    main()