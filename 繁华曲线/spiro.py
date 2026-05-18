import os
os.environ['TCL_LIBRARY'] = r'C:\Users\HP\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\HP\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

import turtle
import math
import random
import argparse
from PIL import Image
from datetime import datetime

# ========= 在这里改画几个，想画3个就改3，画5个就改5 =========
SPIRO_COUNT = 5  
# ==========================================================

class Spiro:
    def __init__(self, xc, yc, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.step = 5
        self.drawing_complete = False

        self.set_parameters(xc, yc, R, r, l)
        self.restart()

    def set_parameters(self, xc, yc, R, r, l):
        self.xc = xc
        self.yc = yc
        self.R = R
        self.r = r
        self.l = l

        gcd_val = math.gcd(self.r, self.R)
        self.n_rot = self.r // gcd_val
        self.k = r / float(R)

        colors = ('blue', 'red', 'green', 'yellow', 'orange', 'purple', 'black','cyan','magenta')
        self.t.color(random.choice(colors))
        self.a = 0

    def restart(self):
        self.drawing_complete = False
        self.t.showturtle()
        self.t.up()
        R, r, l, k = self.R, self.r, self.l, self.k
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        R, r, l, k = self.R, self.r, self.l, self.k
        for i in range(0, self.n_rot * 360 + 1, self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()

    def update(self):
        if self.drawing_complete:
            return
        R, r, l, k = self.R, self.r, self.l, self.k
        a = math.radians(self.a)
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.a += self.step
        if self.a > self.n_rot * 360:
            self.drawing_complete = True
            self.t.hideturtle()

    def clear(self):
        self.t.up()
        self.t.clear()

def saveDrawing():
    turtle.hideturtle()
    dateStr = datetime.now().strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    print('saving drawing to {}.eps/png'.format(fileName))
    try:
        canvas = turtle.getcanvas()
        canvas.postscript(file=fileName + '.eps')
        img = Image.open(fileName + '.eps')
        img.save(fileName + '.png', 'png')
    except:
        pass
    turtle.showturtle()

class SpiroAnimator:
    def __init__(self, N):
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.margin = 100   # 窗口边距，防止出界
        self.restarting = False
        self.spiros = []
        self.spiro_info = []  # 存每个图案的中心+半径，用来判重叠

        for i in range(N):
            # 循环生成 直到找到不重叠的位置
            while True:
                params = self.get_random_params()
                xc, yc, R, r, l = params
                # 检查和已有的是否重叠
                overlap = False
                for (x0,y0,R0) in self.spiro_info:
                    dist = math.hypot(xc-x0, yc-y0)
                    if dist < R + R0 + 30:  # 预留30像素间隔，彻底不挨在一起
                        overlap = True
                        break
                if not overlap:
                    self.spiro_info.append((xc, yc, R))
                    spiro = Spiro(*params)
                    self.spiros.append(spiro)
                    break
        turtle.ontimer(self.update, self.deltaT)

    def get_random_params(self):
        width, height = self.width, self.height
        max_R = min(width, height) // 2 - self.margin
        R = random.randint(50, max_R)
        r = random.randint(10, 9 * R // 10)
        l = random.uniform(0.2, 0.8)
        xc = random.randint(-max_R, max_R)
        yc = random.randint(-max_R, max_R)
        return (xc, yc, R, r, l)

    def update(self):
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawing_complete:
                nComplete += 1
        if nComplete == len(self.spiros):
            self.restart()
        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

    def restart(self):
        if self.restarting:
            return
        self.restarting = True
        # 清空旧数据
        self.spiro_info.clear()
        for spiro in self.spiros:
            spiro.clear()
        # 重新生成不重叠的新图案
        for i in range(len(self.spiros)):
            while True:
                params = self.get_random_params()
                xc, yc, R, r, l = params
                overlap = False
                for (x0,y0,R0) in self.spiro_info:
                    dist = math.hypot(xc-x0, yc-y0)
                    if dist < R + R0 + 30:
                        overlap = True
                        break
                if not overlap:
                    self.spiro_info.append((xc, yc, R))
                    self.spiros[i].set_parameters(*params)
                    self.spiros[i].restart()
                    break
        self.restarting = False

def main():
    print('generating spirograph...')
    descStr = """这个程序使用模块turtle绘制繁花曲线
如果运行时没有指定参数，这个程序将绘制随机的繁花曲线
参数说明如下
R: 外圆半径
r: 内圆半径
l: 孔洞距离与r与R的比值"""
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")
    args = parser.parse_args()

    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title("Spirographs!")
    turtle.onkey(saveDrawing, "s")
    turtle.listen()
    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        spiro = Spiro(0, 0, params[0], params[1], params[2])
        spiro.draw()
    else:
        # 用上面设置的数量
        spiroAnim = SpiroAnimator(SPIRO_COUNT)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")

    turtle.done()

if __name__ == '__main__':
    main()