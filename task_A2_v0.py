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
fig.suptitle('Аналитическая геометрия. А2.')
ax = fig.add_subplot(111)
l = ax.plot([p1[0],p2[0]], [p1[1],p2[1]])
l1 = ax.plot([p3[0],p4[0]], [p3[1],p4[1]])


#
def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return
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

point = (seg_intersect( p1,p2, p3,p4))
if type(point)==bool:
    print("Отрезки параллельны или лежат на одной прямой.")
elif (min(p1[0],p2[0])<=point[0]<=max(p1[0],p2[0]) and min(p1[1],p2[1])<=point[1]<=max(p1[1],p2[1])
    and min(p3[0],p4[0])<=point[0]<=max(p3[0],p4[0])and min(p3[1],p4[1])<=point[1]<=max(p3[1],p4[1])):
    print ("Точка пересечения отрезков (%.2f, %.2f)" %(point[0],point[1]))
    ax.plot(point[0],point[1], 'ro')
else: print("Отрезки не пересекаются.")
plt.show()
