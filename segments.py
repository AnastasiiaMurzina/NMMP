import matplotlib.pyplot as plt
from numpy.linalg import solve
from numpy import array

def reader_coords(file_name): # чтение из файла два вектора координат
    xs, ys = [], []
    with open(file_name, 'r') as f:
        for line in f:
            x, y = line.split(',')
            xs.append(int(x))
            ys.append(int(y))
    return xs, ys

def cross_checker(xs12, ys12, xs23, ys23): # находим пересечения
    line1 = solve(array([[xs12[0], 1], [xs12[1], 1]]), array(ys12)) # находим коэффициенты прямой y=a*x+b
    line2 = solve(array([[xs23[0], 1], [xs23[1], 1]]), array(ys23)) # для каждого из отрезков
    if line1[0] == line2[0]: # если они параллельны, то считаем, что они не пересекаются
        return []
    point = solve(array([[1, -line1[0]], [1, -line2[0]]]), array([line1[1], line2[1]])) # находим точку пересечения
    if min(xs12) <= point[1] <= max(xs12) and min(xs23) <= point[1] <= max(xs23)\
            and min(ys12) <= point[0] <= max(ys12) and min(ys23) <= point[0] <= max(ys23):
        # после проверки, что это точка лежит на отрезках возвращаем эту точку
        return point
    return []


if __name__ == '__main__':
    file = 'segments.txt'
    xs, ys = reader_coords(file)
    # ax = plt.subplot(111)
    plt.plot(xs, ys) # нарисовали отрезки
    for i in range(2, len(xs)-1): # начиная с третьего отрезка
        for j in range(i-1): # проверяем пересечения с предыдущими отрезками, кроме предыдущего
            point = cross_checker(xs[i:i+2], ys[i:i+2], xs[j:j+2], ys[j:j+2])
            if len(point) == 2: plt.scatter(point[1], point[0], c='r') # если пересечение есть рисуем его красной точкой
    plt.savefig('segments.png') #сохранили картинку
    plt.show() #показать
