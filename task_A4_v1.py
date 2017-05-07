import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def main():

    point0 = input("Введите координаты начала отрезка через пробел ").split()
    point_x0=float(point0[0])
    point_y0 = float(point0[1])
    point1 = input("Введите координаты конца отрезка ").split()
    point_x1 = float(point1[0])
    point_y1 = float(point1[1])
    c = input("Введите координаты цетра окружности").split()
    circle_x = float(c[0])
    circle_y = float(c[1])
    radius = float(input("Введите радиус окружности "))

    fig = plt.figure()  #
    fig.suptitle('Аналитическая геометрия. Б1')
    ax = fig.add_subplot(111)
    floor = Circle((circle_x, circle_y), radius, alpha=0.5) #alpha - прозрачность
    ax.add_patch(floor)
    l = ax.plot([point_x0, point_x1], [point_y0, point_y1])

    #############################################
    if point_x0==point_x1: #если отрезок вертикален - меняем оси
        swap = point_x0 # тогда избегаем деления на 0
        point_x0=point_y0
        point_y0 =swap
        swap = point_x1
        point_x1 = point_y1
        point_y1 = swap
        swap = circle_x
        circle_x=circle_y
        circle_y=swap
    else: swap='' # своебразный флаг на проверку смены осей
    x0 = min(point_x0, point_x1) #упорядочиваем границы, для которых проверяем пересечение
    x1 = max(point_x0, point_x1)
    y0 = min(point_y0, point_y1)
    y1 = max(point_y0, point_y1)
    a = (point_y1 - point_y0) / (point_x1 - point_x0)
    b = point_y0 - a * point_x0 # нашли коэффициенты для прямой, содержащей отрезок
    discr = (a * b - a * circle_y - circle_x) ** 2 - (a ** 2 + 1) * (
    circle_x ** 2 + b ** 2 + circle_y ** 2 - radius ** 2) #дискременант из уравнения пересечения прямой
    # и окружности
    if discr == 0:  # одна точка пересечения
        result_x = -(a * b - a * circle_y - circle_x) / (a ** 2 + 1) #решение квадратного уравнения
        result_y = a * result_x + b
        if x0 <= result_x <= x1 and y0 <= result_y <= y1: # пренадлежит ли найденное решение отрезку?
            if type(swap)!=str: #если меняли оси - меняем их обратно
                swap=result_y
                result_y = result_x
                result_x = swap
                print("Точка персечения отрезка A(%f, %f) - B(%f, %f) и окружности C(%f,%f, r=%f)"
                      % (point_y0, point_x0, point_y1, point_x1, circle_y, circle_x, radius))
                # вывод результата для данного случая
            else:print("Точка персечения отрезка A(%f, %f) - B(%f, %f) и окружности C(%f,%f, r=%f)"
                      %(point_x0, point_y0,point_x1,point_y1,circle_x,circle_y,radius))
            # вывод, когда не меняли оси
            plt.plot([result_x], [result_y], marker='o') #выводим результирующую точку на график
        else: print("Не пересекаются") # если точка есть на прямой, но не на отрезке
    elif discr > 0: #две точки
        result_x = (-(a * b - a * circle_y - circle_x) + discr ** 0.5) / (a ** 2 + 1)
        result_y = a * result_x + b
        if x0 <= result_x <= x1 and y0 <= result_y <= y1:
            if type(swap)!=str:
                swap=result_y
                result_y = result_x
                result_x = swap
                print("Точка персечения отрезка A(%f, %f) - B(%f, %f) и окружности C(%f,%f, r=%f) имеет координаты (%f, %f) "
                      %(point_y0, point_x0,point_y1,point_x1,circle_y,circle_x,radius,result_x,result_y))
            else:print("Точка персечения отрезка A(%f, %f) - B(%f, %f) и окружности C(%f,%f, r=%f) имеет координаты (%f, %f) "
                           % (point_x0, point_y0, point_x1, point_y1, circle_x, circle_y, radius,result_x,result_y))
            plt.plot([result_x], [result_y], marker='o')

        else:
            print("Не пересекаются")
        result_x = (-(a * b - a * circle_y - circle_x) - discr ** 0.5) / (a ** 2 + 1)
        result_y = a * result_x + b

        if x0 <= result_x <= x1 and y0 <= result_y <= y1:
            if type(swap)!=str:
                swap=result_y
                result_y = result_x
                result_x = swap
                print("Точка персечения отрезка A(%f, %f) - B(%f, %f) и окружности C(%f,%f, r=%f) имеет координаты (%f, %f) "
                      % (point_y0, point_x0, point_y1, point_x1, circle_y, circle_x, radius,result_x,result_y))
            else:print("Точка персечения отрезка A(%f, %f) - B(%f, %f) и окружности C(%f,%f, r=%f) имеет координаты (%f, %f) "
                      %(point_x0, point_y0,point_x1,point_y1,circle_x,circle_y,radius,result_x,result_y))
            plt.plot([result_x], [result_y], marker='o')
        else:
            print("Не пересекаются")
    else:
        print("Не пересекаются")
    #############################################
    plt.show()
    return 0

if __name__ == '__main__':
    main()