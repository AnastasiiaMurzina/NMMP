import matplotlib.pyplot as plt
import numpy as np
 #ввод параметров
p1 = input("Введите координаты начала первого отрезка").split()
p1 = np.array([float(p1[0]), float(p1[1])])
p2 = input("Введите координаты конца первого отрезка").split()
p2 = np.array([float(p2[0]), float(p2[1])])
p3 = input("Введите координаты начала второго отрезка").split()
p3 = np.array([float(p3[0]), float(p3[1])])
p4 = input("Введите координаты конца второго отрезка").split()
p4 = np.array([float(p4[0]), float(p4[1])])
fig = plt.figure()  # график
fig.suptitle('Аналитическая геометрия. А3.')
ax = fig.add_subplot(111)
l = ax.plot([p1[0],p2[0]], [p1[1],p2[1]])
l1 = ax.plot([p3[0],p4[0]], [p3[1],p4[1]])


#
def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1 #  "вектор" первого отрезка
    db = b2-b1#  "вектор"  второго отрезка
    dp = a1-b1 # вектор, соединяющий начала отрезков
    dap = perp(da) #перпендикуляр к последнему
    denom = np.dot( dap, db) #проекция одного на другом
    num = np.dot( dap, dp )
    if (denom)==0: #если перпендикуляр перпендикуляра перпендикулярен, то они параллельны
        return False
    return (num / denom.astype(float))*db + b1 #иначе точка пересечения гарантированно одна


def distance(p1, p2, point0):
    if p1[0] == p2[0]:  # если прямая вертикальна
        p1[0], p1[1] = [p1[1], p1[0]]  # избегаем /0 сменой осей
        p2[0], p2[1] = [p2[1], p2[0]]
        point0[0], point0[1] = [point0[1], point0[1]]
    a = (p1[1] - p2[1]) / (p1[0] - p2[0])  # угол наклона отрезка
    b = p1[1] - a * p1[0]  # y=ax+b
    result_x = (point0[0] + a * point0[1] - a * b) / (
        a ** 2 + 1)  # из равенства производной нулю при нахождения минимума растояния
    if result_x < min(p1[0], p2[0]):
        result_x = min(p1[0],
                       p2[0])  # если x левее отрезка, то наиближайшей будет точка с самой левой координатой отрезка
    elif result_x > max(p1[0], p1[1]):
        result_x = max(p2[0], p2[1])  # иначе с самой правой
    result_y = a * result_x + b  # у соответсвующий найденному х
    result = ((result_x - point0[0]) ** 2 + (result_y - point0[1]) ** 2) ** 0.5  # нашли расстояние
    if a == 0:  # если меняли оси
        result_y, result_x = [result_x, result_y]

    return result_x, result_y

point = (seg_intersect( p1,p2, p3,p4))
if type(point)==bool:
    print("Отрезки параллельны или лежат на одной прямой. Найдём расстояние между прямыми, содержащими отрезки")
    dac = p3 - p1
    dad = p4 - p1
    dbc = p3 - p2
    dbd = p4 - p2
    print("Расстояние между прямыми = %.2f" %min(list(map( lambda x: np.linalg.norm(x),[dac,dad,dbc,dbd]))).append(abs(np.dot(dac, perp(p2-p1)))))

elif (min(p1[0],p2[0])<=point[0]<=max(p1[0],p2[0]) and min(p1[1],p2[1])<=point[1]<=max(p1[1],p2[1])
    and min(p3[0],p4[0])<=point[0]<=max(p3[0],p4[0])and min(p3[1],p4[1])<=point[1]<=max(p3[1],p4[1])):
    print ("Отрезки пересекаются, расстояние между ними = 0" )
    ax.plot(point[0],point[1], 'ro')

else:
    cross_point1 = (distance(p1,p2,point))
    cross_point2 = (distance(p3, p4, point))
    ax.plot([cross_point1[0],cross_point2[0]],[cross_point1[1],cross_point2[1]], 'k--')
    dist = ((cross_point2[1]-cross_point1[1])**2+(cross_point2[0]-cross_point1[0])**2)**0.5
    print("Расстояние между отрезками = " + str(dist))
plt.show()
