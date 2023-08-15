# ʹ��Python��turtle��ʵ���߶�����ܻ���
# https://www.cnblogs.com/shenxiaolin/p/8471226.html
import turtle, datetime
def drawLine1(draw):  # ���Ƶ��������
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    turtle.right(90)
def drawDigit1(digit):  # �������ֻ����߶������
    drawLine1(True) if digit in [2, 3, 4, 5, 6, 8, 9] else drawLine1(False)
    drawLine1(True) if digit in [0, 1, 3, 4, 5, 6, 7, 8, 9] else drawLine1(False)
    drawLine1(True) if digit in [0, 2, 3, 5, 6, 8, 9] else drawLine1(False)
    drawLine1(True) if digit in [0, 2, 6, 8] else  drawLine1(False)
    turtle.left(90)
    drawLine1(True) if digit in [0, 4, 5, 6, 8, 9] else drawLine1(False)
    drawLine1(True) if digit in [0, 2, 3, 5, 6, 7, 8, 9] else drawLine1(False)
    drawLine1(True) if digit in [0, 1, 2, 3, 4, 7, 8, 9] else drawLine1(False)
    turtle.left(180)
    turtle.penup()
    turtle.fd(20)
def drawDate1(date):  # ���Ҫ���������
    for i in date:
        drawDigit1(eval(i))  # ע��: ͨ��eval()���������ֱ�Ϊ����

def main1():
    turtle.setup(800, 350, 200, 200)
    turtle.penup()
    turtle.fd(-300)
    turtle.pensize(5)
    drawDate1(datetime.datetime.now().strftime('%Y%m%d'))
    turtle.hideturtle()

main1()