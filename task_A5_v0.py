import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def main():
    point0 = input("Введите координаты центра окружности через пробел ").split()
    point_x0=float(point0[0])
    point_y0 = float(point0[1])
    radius0 = float(input("Введите радиус окружности "))
    point1 = input("Введите координаты центра другой окружности ").split()
    point_x1 = float(point1[0])
    point_y1 = float(point1[1])
    radius1 = float(input("Введите радиус окружности "))
    fig = plt.figure()  #
    fig.suptitle('Аналитическая геометрия. Б2')
    ax = fig.add_subplot(111)
    ax.set_xlim(min(point_x0 - radius0, point_x1 - radius1) - 1, max(point_x0 + radius0, point_x1 + radius1) + 1)
    ax.set_ylim(min(point_y0 - radius0, point_y1 - radius1) - 1, max(point_y0 + radius0, point_y1 + radius1) + 1)
    floor = Circle((point_x0, point_y0), radius0, alpha=0.5)
    ax.add_patch(floor)
    floor2 = Circle((point_x1, point_y1), radius1, alpha=0.5)
    ax.add_patch(floor2)
    if [point_x0,point_y0,radius0]==[point_x1,point_y1,radius1]:
        print("Окружности совпадают")
    elif [point_x0,point_y0]==[point_x1,point_y1]:
        print("Общий центр,они не пересекаются")
    else:
        if point_y0==point_y1:
            # print("they are equal")
            # print(point_y0,point_y1)
            swap = point_x0
            point_x0 = point_y0
            point_y0 = swap
            swap = point_x1
            point_x1 = point_y1
            point_y1 = swap
            # print(point_y0,point_y1)
        else: swap=''
        y =lambda x: (2*x*(point_x0-point_x1)+point_x1**2-point_x0**2+radius0**2-radius1**2+point_y1**2-point_y0**2)/(2*(point_y1-point_y0))
        alpha = (point_x0-point_x1)/(point_y1-point_y0)
        c = (point_x1**2-point_x0**2+radius0**2-radius1**2+point_y1**2-point_y0**2)/(2*(point_y1-point_y0))
        koeff_a=(1+alpha**2)
        koeff_b = (alpha*c-alpha*point_y0-point_x0)
        koeff_c = point_x0**2+c**2-2*point_y0*c+point_y0**2-radius0**2
        discr = (koeff_b**2-koeff_a*koeff_c)
        if discr >=0:
            result_x = (-koeff_b+discr**0.5)/koeff_a
            result_y = y(result_x)
            if swap!='':
                swap = result_x
                result_x = result_y
                result_y = swap
                print("Пересечение окружносте C1(%f,%f), r1=%f и C2(%f, %f), r2= %f в точке (%f, %f)"
                      %(point_y0,point_x0,radius0,point_y1,point_x1,radius1,result_x,result_y))
            else:
                print("Пересечение окружносте C1(%f,%f), r1=%f и C2(%f, %f), r2= %f в точке (%f, %f)"
                      % (point_x0, point_y0, radius0, point_x1, point_y1, radius1, result_x, result_y))
            po = [[result_x,result_y],]
            plt.plot(*zip(*po), marker='o', color='r', ls='')
            result_x = (-koeff_b - discr ** 0.5) / koeff_a
            result_y = y(result_x)
            if swap!='':
                swap = result_x
                result_x = result_y
                result_y = swap
                print("Пересечение окружносте C1(%f,%f), r1=%f и C2(%f, %f), r2= %f в точке (%f, %f)"
                      % (point_y0, point_x0, radius0, point_y1, point_x1, radius1, result_x, result_y))
            else: print("Пересечение окружносте C1(%f,%f), r1=%f и C2(%f, %f), r2= %f в точке (%f, %f)"
                      % (point_x0, point_y0, radius0, point_x1, point_y1, radius1, result_x, result_y))
            po = [[result_x, result_y], ]
            plt.plot(*zip(*po), marker='o', color='r', ls='')


    #############################################

    plt.show()
    return 0

if __name__ == '__main__':
    main()