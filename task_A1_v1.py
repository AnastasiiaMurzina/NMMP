import matplotlib.pyplot as plt

def main(): #рассматриваю отрезок как прямую
    point = input("Введите координаты точки через пробел ").split()
    point_x=float(point[0])
    point_y = float(point[1])
    line_segment_0 = input("Введите координаты начала отрезка ").split()
    l_seg_0_x = float(line_segment_0[0])
    l_seg_0_y = float(line_segment_0[1])
    line_segment_1 = input("Введите координаты конца отрезка ").split()
    l_seg_1_x = float(line_segment_1[0])
    l_seg_1_y = float(line_segment_1[1])

    fig = plt.figure()  # готовим figure для вывода графика
    fig.suptitle('Аналитическая геометрия. А1')
    ax = fig.add_subplot(111)
    po = [[point_x, point_y], ]
    plt.plot(*zip(*po), marker='o', color='r', ls='')  # вывод точки на график
    l = ax.plot([l_seg_0_x, l_seg_1_x], [l_seg_0_y, l_seg_1_y])  # вывод отрезка
    ax.set_xlim(min(l_seg_0_y,l_seg_1_y,point_y,l_seg_0_x,l_seg_1_x,point_x)-1,
                max(l_seg_0_x,l_seg_1_x,point_x,l_seg_0_y,l_seg_1_y,point_y)+1)
    # фиксируем границы, чтоб изображение
    ax.set_ylim(min(l_seg_0_x,l_seg_1_x,point_x,l_seg_0_y,l_seg_1_y,point_y)-1,
                max(l_seg_0_x,l_seg_1_x,point_x,l_seg_0_y,l_seg_1_y,point_y)+1)

    #############################################

    if l_seg_0_x==l_seg_1_x: #если прямая вертикальна
        l_seg_0_x, l_seg_0_y = [l_seg_0_y, l_seg_0_x] #избегаем /0 сменой осей
        l_seg_1_x,l_seg_1_y=[l_seg_1_y,l_seg_1_x]
        point_x,point_y=[point_y,point_x]

    a = (l_seg_0_y-l_seg_1_y)/(l_seg_0_x-l_seg_1_x) # угол наклона отрезка
    b = l_seg_0_y - a * l_seg_0_x  # y=ax+b
    result_x = (point_x+a*point_y-a*b)/(a**2+1) #из равенства производной нулю при нахождения минимума растояния
    if result_x<min(l_seg_0_x,l_seg_1_x): result_x =min(l_seg_0_x,l_seg_1_x) #если x левее отрезка, то наиближайшей будет точка с самой левой координатой отрезка
    elif result_x>max(l_seg_0_x,l_seg_1_x): result_x = max(l_seg_0_x,l_seg_1_x) #иначе с самой правой
    result_y=a*result_x+b # у соответсвующий найденному х
    result = ((result_x-point_x)**2+(result_y-point_y)**2)**0.5  #нашли расстояние
    if a==0: #если меняли оси
        print('Расстояние между отрезком A(%f, %f) - B(%f, %f) и точкой C(%f, %f) = %f' % (l_seg_0_y, l_seg_0_x,
                                                                                           l_seg_1_y, l_seg_1_x,
                                                                                           point_y, point_x, result))
        ax.plot([result_y,point_y],[result_x,point_x],'k--')
        print(point_x,point_y)
    else: #если не меняли
        print('Расстояние между отрезком A(%f, %f) - B(%f, %f) и точкой C(%f, %f) = %f' %(l_seg_0_x, l_seg_0_y,
          l_seg_1_x,l_seg_1_y,point_x,point_y, result))
        ax.plot([result_x, point_x], [result_y, point_y], 'k--')

#############################################
    plt.show()
    return 0

"""Программа работает корректно (возможно?). Прежде чем искать ошибки в алгоритме/коде:
 нужно посчтитать другие возможные наикрайтчайшие расстояния, т.к. масштаб графика искажён!
 Если прерывистая линия будет совсем не там - пиши - буду исправлять."""

if __name__ == '__main__':
    main()