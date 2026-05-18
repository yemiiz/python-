import math
import turtle

def draw_circle(x, y, r):
    #   1.  turtle.circle(r)可以直接画圆，但这里我们用更基本的方法来画圆，以便更好地理解圆的绘制过程。
    #  2.  turtle.up()和turtle.down()分别用于抬起和放下画笔，以便在移动到起始位置时不留下痕迹。
    turtle.up()
    turtle.goto(x + r,y)    #也可以用setpos
    turtle.down()

    for angle in range(0, 360, 5): #每隔5度计算一个点，形成一个多边形来近似圆，也可以不加默认1
        px = x + r * math.cos(math.radians(angle)) #math.radians(angle)将角度转换为弧度，因为math.cos和math.sin函数需要弧度作为输入。
        py = y + r * math.sin(math.radians(angle))
        turtle.goto(px, py)
    #并不是真正的画圆，而是通过计算每个角度对应的点来模拟画圆的过程，是正多边形的一个特例，角度越多，圆就越平滑。
def main():
    radius = float(input("Enter the radius of the circle: "))
    draw_circle(0, 0, radius)
    turtle.done()
if __name__ == "__main__":    main()