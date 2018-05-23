import matplotlib.pyplot as plt
from numpy import array
from numpy.linalg import solve, norm
from itertools import product, combinations


def read_polys(file): # считаем многоугольники из файла
    with open(file, 'r') as f:
        n1, n2 = list(map(int, f.readline().split())) #первая строчка файла - количество углов многоугольников
        a, b = [], []
        for _ in range(n1): # координаты первого
            a.append(list(map(float, f.readline().split())))
        f.readline()
        for _ in range(n2): #второго
            b.append(list(map(float, f.readline().split())))
        return a, b


def abs_borders(polygon): # находим крайние точки у многоугольника
    left_right = sorted(polygon) # сортируем по х-ам и берём левого и правого
    l_prd = left_right[0] # которые могут оказаться не единственными, поэтому может
    r_pru = left_right[-1] # получится, что мы возьмём левого-нижнего, правго-верхнего...
    down_up = sorted(polygon, key=lambda x: x[1]) # сортировка по у-ам
    d_prl = down_up[0]
    up_prr = down_up[-1]
    return l_prd, up_prr, r_pru, d_prl # левый, верхний, правый, нижний


def from_point(point, s1, s2): # ближайшая точка и расстояние до неё
    v = array(s2) - array(s1)
    u = array(s1) - array(point)
    t = -(v[0]*u[0]+v[1]*u[1])/norm(v)**2 # параметрическое задание отрезка
    if t < 0: # если ближайщая точка вне отрезка и ближе к s1
        p = array(s1)
    elif t > 1:
        p = array(s2)
    else: # если точка на отрезке
        p = (1-t)*array(s1)+t*array(s2)
    return p[0], p[1], norm(array(point-p))


def checker(a, b): # проверка как расположены многоугольники
    la, ua, ra, da = abs_borders(a)
    lb, ub, rb, db = abs_borders(b)
    ds = []
    flag = True # флаг пересечения
    if ua > ub and da < db and la < lb and ra > rb:
        print('B in A')
        for i, j in product(range(len(a)-1), range(len(b)-1)):
            bs = between_segments(a[i], a[i + 1], b[j], b[j + 1])
            if bs:
                ds.append(bs)
    elif ua < ub and da > db and la > lb and ra < rb:
        print('A in B')
        for i, j in product(range(len(a)-1), range(len(b)-1)):
            bs = between_segments(a[i], a[i + 1], b[j], b[j + 1])
            if bs:
                ds.append(bs)
    elif (ua < ub and da > db) or (la < lb and ra < rb) or (ua > ub and da < db)\
            or (la > lb and ra > rb):
        print('Многогранники пересекаются, расстояние между ними 0')
        flag = False
    else:
        print('Outside')
    return flag


def between_segments(s1, s2, e1, e2):
    x1, y1 = s1
    x2, y2 = s2
    x3, y3 = e1
    x4, y4 = e2
    if(x1-x2)*(y3-y4) != (y1-y2)*(x3-x4): # если стороны непараллельны - ищем пересечени
        intersection = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)), ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    else:
        return # пока что не обрабатываем, сложно(
    if min(x1, x2) < intersection[0] < max(x1, x2) and min(y1, y2) < intersection[1] < max(y1, y2): # если пересечение попало на один из отрезков
        if (intersection[0]-x3)**2 + (intersection[1]-y3)**2 < (intersection[0]-x4)**2 + (intersection[1]-y4)**2:
            return [((intersection[0]-x3)**2 + (intersection[1]-y3)**2)**0.5, [intersection[0], intersection[1]], [x3, y3]]
        else:
            return [((intersection[0] - x4) ** 2 + (intersection[1] - y4) ** 2)**0.5, [intersection[0], intersection[1]], [x4, y4]]
    elif min(x3, x4) < intersection[0] < max(x3, x4) and min(y3, y4) < intersection[1] < max(y3, y4): # если на другой
        if (intersection[0]-x1)**2 + (intersection[1]-y1)**2 < (intersection[0]-x2)**2 + (intersection[1]-y2)**2:
            return [((intersection[0]-x1)**2 + (intersection[1]-y1)**2)*0.5, [intersection[0], intersection[1]], [x1, y1]]
        else:
            return [((intersection[0] - x2) ** 2 + (intersection[1] - y2) ** 2)**0.5, [intersection[0], intersection[1]], [x2, y2]]
    else:
        a = (x1-intersection[0])**2+(y1-intersection[1])**2
        b = (x3 - intersection[0])**2 + (y3-intersection[1])**2
        c = (x1-x3)**2+(y1-y3)**2
        d1 = (x2 - intersection[0]) ** 2 + (y2 - intersection[1]) ** 2
        d2 = (x4 - intersection[0]) ** 2 + (y4 - intersection[1]) ** 2
        if a+b < c: # угол при пересекающихся отрезках тупой
            if a < d1:
                p1 = [x1, y1]
            else:
                p1 = [x2, y2]
            if b < d2:
                p2 = [x3, y3]
            else:
                p2 = [x4, y4]
        else: # угол-таки острый
            mm = min([a, b, d1, d2])
            if a == mm or d1 == mm:
                if d2 < b:
                    p1 = [x4, y4]
                else:
                   p1 = [x3, y3]
                x, y, d = from_point(p1, [x1, y1], [x2, y2])
                p2 = [x, y]
            else:
                if d1 < a:
                    p1 = [x2, y2]
                else:
                    p1 = [x1, y1]
                x, y, d = from_point(p1, [x3, y3], [x4, y4])
                p2 = [x, y]
        return [((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5, p1, p2]

if __name__ == '__main__':
    a, b = read_polys('polys.txt')
    a.append(a[0]) # замыкаем многоугольники
    b.append(b[0])
    if checker(a, b): # если не пересекаются, то считаем расстояние
        ds = []
        for i, j in product(range(len(a)-1), range(len(b)-1)): # для каждой пар сторон считаем расстояние
            dpp = between_segments(a[i], a[i+1], b[j], b[j+1])
            if dpp: # программа пока что не считает расстояние между параллельными сторонами
                d, p1, p2 = dpp
                ds.append([d, p1, p2])
        mpoints = sorted(ds)[0] # кратчайшее
        print('Расстояние', mpoints[0])
        plt.plot([mpoints[1][0], mpoints[2][0]], [mpoints[1][1], mpoints[2][1]])
    plt.plot([i[0] for i in a], [i[1] for i in a])
    plt.plot([i[0] for i in b], [i[1] for i in b])
    plt.show()
