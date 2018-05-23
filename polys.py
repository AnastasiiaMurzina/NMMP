import matplotlib.pyplot as plt
from numpy import array
from numpy.linalg import solve, norm
from itertools import product, combinations


def read_polys(file):
    with open(file, 'r') as f:
        n1, n2 = list(map(int, f.readline().split()))
        a, b = [], []
        for _ in range(n1):
            a.append(list(map(float, f.readline().split())))
        f.readline()
        for _ in range(n2):
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


def from_point(point, s1, s2):
    a = s2[1]-s1[1]
    b = s1[0]-s2[0]
    c = -a*s1[0] -b*s1[1]#s2[0]*s1[1] - s2[1]*s1[0]
    ab = a**2+b**2
    pr_d = abs(a*point[0]+b*point[1]+c)/ab**0.5
    # v = array(s2)-array(s1)
    # u = array(s1) - array(point)
    # x = v[0]*u[1]/norm(v)+point[0]
    # y = -v[1]*u[0]/norm(v)+point[1]
    # x, y =(v*u/norm(v))
    # v =array([a, b])
    # v /= norm(v)*pr_d
    # v += point
    x = (-b*(-b*point[0] + a*point[1])-a*c)/ab
    y = (a*(-b*point[0] + a*point[1])-b*c)/ab
    # if min(s1[0], s2[0]) < x < max(s1[0], s2[0]) and min(s1[1], s2[1]) < y < max(s1[1], s2[1]):
    #     print(x, y)
    return pr_d, x, y
    # elif (s1[0]-point[0])**2+(s1[1]-point[1])**2 < (s2[0]-point[0])**2+(s2[1]-point[1])**2:
    #     return (s1[0]-point[0])**2+(s1[1]-point[1])**2, s1[0], s1[1]
    # return (s2[0] - point[0]) ** 2 + (s2[1] - point[1]) ** 2, s2[0], s2[1]


def between_segments(s1, s2, e1, e2):
    x1, y1 = s1
    x2, y2 = s2
    x3, y3 = e1
    x4, y4 = e2
    if(x1-x2)*(y3-y4) != (y1-y2)*(x3-x4):
        intersection = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)), ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    else:
        return
    if min(x1, x2) < intersection[0] < max(x1, x2) and min(y1, y2) < intersection[1] < max(y1, y2): # если пересечение попало на один из отрезков
        if (intersection[0]-x3)**2 + (intersection[1]-y3)**2 < (intersection[0]-x4)**2 + (intersection[1]-y4)**2:
            return [((intersection[0]-x3)**2 + (intersection[1]-y3)**2)**0.5, [intersection[0], intersection[1]], [x3, y3]]
        else:
            return [((intersection[0] - x4) ** 2 + (intersection[1] - y4) ** 2)**0.5, [intersection[0], intersection[1]], [x4, y4]]
    elif min(x3, x4) < intersection[0] < max(x3, x4) and min(y3, y4) < intersection[1] < max(y3, y4):
        if (intersection[0]-x1)**2 + (intersection[1]-y1)**2 < (intersection[0]-x2)**2 + (intersection[1]-y2)**2:
            return [((intersection[0]-x1)**2 + (intersection[1]-y1)**2)*0.5, [intersection[0], intersection[1]], [x1, y1]]
        else:
            return [((intersection[0] - x2) ** 2 + (intersection[1] - y2) ** 2)**0.5, [intersection[0], intersection[1]], [x2, y2]]
    else:
        a = (x1-intersection[0])**2+(y1-intersection[1])**2
        b = (x3 - intersection[0])**2 + (y3-intersection[1])**2
        c = (x1-x3)**2+(y1-y3)**2
        if (a+b-c) < 0: # угол при пересекающихся отрезках тупой
            if a < (x2 - intersection[0])**2 + (y2-intersection[1])**2:
                p1 = [x1, y1]
            else:
                p1 = [x2, y2]
            if b < (x3 - intersection[0])**2 + (y3 - intersection[1])**2:
                p2 = [x3, y3]
            else:
                p2 = [x4, y4]
        else: # угол-таки острый
            d1 = (x2 - intersection[0])**2 + (y2-intersection[1])**2
            d2 = (x4 - intersection[0])**2 + (y4 - intersection[1])**2
            mm = min([a, b, d1, d2])
            if a == mm or d1 == mm:
                if d2 < b:
                    p1 = [x4, y4]
                else:
                    p1 = [x3, y3]
                if a == mm:
                    p2 = from_point([x1, y1], [x3, y3], [x4, y4])[1:]
                    if not(x3 < p2[0] < x4 and y3 < p2[1] < y4):
                        if (p1[0]-x3)**2+(p1[1]-y3)**2 < (p1[0]-x4)**2+(p1[1]-y4)**2:
                            p2 = [x3, y3]
                        else:
                            p2 = [x4, y4]
                else:
                    p2 = from_point([x2, y2], [x3, y3], [x4, y4])[1:]
                    if not(x3 < p2[0] < x4 and y3 < p2[1] < y4):
                        if (p1[0]-x3)**2+(p1[1]-y3)**2 < (p1[0]-x4)**2+(p1[1]-y4)**2:
                            p2 = [x3, y3]
                        else:
                            p2 = [x4, y4]
            else:
                if d1 < a:
                    p1 = [x2, y2]
                else:
                    p1 = [x1, y1]
                if b == mm:
                    p2 = from_point([x3, y3], [x1, y1], [x2, y2])[1:]
                    if not(x1 < p2[0] < x2 and y1 < p2[1] < y2):
                        if (p1[0]-x1)**2+(p1[1]-y1)**2 < (p1[0]-x2)**2+(p1[1]-y2)**2:
                            p2 = [x1, y1]
                        else:
                            p2 = [x2, y2]
                else:
                    p2 = from_point([x4, y4], [x1, y1], [x2, y2])[1:]
                    if not(x1 < p2[0] < x2 and y1 < p2[1] < y2):
                        if (p1[0]-x1)**2+(p1[1]-y1)**2 < (p1[0]-x2)**2+(p1[1]-y2)**2:
                            p2 = [x1, y1]
                        else:
                            p2 = [x2, y2]
        return [((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5, p1, p2]



def checker(a, b):
    la, ua, ra, da = abs_borders(a)
    lb, ub, rb, db = abs_borders(b)
    ds = []
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
    else:
        print('Outside')
        ps = []
        for j, i in product(range(len(a)-1), range(len(b)-1)):
            # bs = between_segments(a[i], a[i + 1], b[j], b[j + 1])
            ix = from_point(b[i], a[j], a[j+1])
            if ix:
                ps.append([b[i], from_point(b[i], a[j], a[j+1])])
        return ps
            #
            # if bs:
            #     ds.append(bs)
    # print(sorted(ds))
    # return (sorted(ds))

if __name__ == '__main__':
    a, b = read_polys('polys.txt')
    la, ua, ra, da = abs_borders(a)
    lb, ub, rb, db = abs_borders(b)
    a.append(a[0])
    b.append(b[0])
    ps = (checker(a, b))
    # p1, p2 = (checker(a, b))
    print(ps)
    # for i in ps:
    i = ps[1]
    plt.plot([i[0][0], i[1][0]], [i[0][1], i[1][1]])
        # plt.plot([i[1][0], i[2][0]], [i[1][1], i[2][1]])
    # plt.plot([p1[0], p2[0]], [p1[1], p2[1]])
    plt.plot([i[0] for i in a], [i[1] for i in a])
    plt.plot([i[0] for i in b], [i[1] for i in b])
    plt.show()
