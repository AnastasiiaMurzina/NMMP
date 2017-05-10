from math import log
from math import atanh
import matplotlib.pyplot as plt

#Константы, которые есть в функциях
g_Earth=9.81
g_Moon=1.622
u=3000.

m0_fluel=100 #начальный запас топлива


def high(M,h0,v0,dm,dt,u): #расчёт высоты
    h=h0-g_Moon*dt**2/2-dt*u*log(1-dm/M)+dt*M*u*log(1-dm/M)/dm+u*dt+v0*dt
    return h

def velocity(M,v0,dm,dt,u):# расчёт скорости
    v=v0-g_Moon*dt-2*u*atanh(dm/(dm-2*M))
    return v

def overheight(M,dm,dt,u):#перегрузка
    return dm/dt*u/M/g_Earth

def main(m0_fluel, u):
    h=1000.#начальная высота
    M0=1000. #сухая масса лунолёта
    M=M0+m0_fluel #масса с топливом
    v=0
    arr_h=[]#инилизируем массив для хранения высот (чтоб вывести график)
    arr_h.append(h)
    arr_v=[]#-\\- скорости
    arr_v.append(v)
    arr_t=[]#-\\- время
    arr_t.append(0)
    print("Необходимо посадить лунолёт с высоты ", h, " метров. С запасом топлива ", m0_fluel, " кг.")
    print("Вводите данные в форматe '{R }dm dt' или '{R,}dm,dt', разделив только запятыми или только пробелами.")
    print("Не вводите 0 для промежутка времени - это бессмыслено и необработано!")
    while(True):
        print("\n")
        string=(input("Введите массу и время выброса топлива:")).split() #разделяем вводные данные по пробелам
        if len(string)==1:#если пробелов нет, но мы уже имеем массив
            string=string[0].split(",")# в этом случае разделяем запятыми
        dt=float(string[len(string)-1])# последнее преобразуем в число - промежуток времени
        dm=min(float(string[len(string)-2]),m0_fluel)# выбрасываемая масса, если пытаемся выбросить больше остатка - выбрасываем всё, что осталось
        if string[0]=='R': u_cur=-abs(u)# проверяем на направление выброса топлива
        else: u_cur=abs(u)
        if m0_fluel!=0:# если есть топливо
            if abs(overheight(M, dm, dt, u_cur)) <= 5:  # проверяем на перегрузку
                if dm == 0:  # если ввели, что не выбрасываем массу
                    dm = 1  # избегаем деления на 0
                    u_cur = 0  # если u=0, то формула преобразуется в нужную, без написания дополнительных функций
                h = high(M, h, v, dm, dt, u_cur)
                v = velocity(M, v, dm, dt, u_cur)  # сначала пересчитываем высоту и скорость
                if u_cur != 0:  # а потом, если тратим топливо(dm=1 чтобы не /0), то мы его сжигаем
                    m0_fluel -= dm
                    M -= dm
                arr_t.append(arr_t[len(arr_t) - 1] + dt)  # в "нормальном" режиме мы можем сразу добавить время
            else:  # если же перегрузка, то:
                print("Перегрузка! Корабль неуправляем")
                h = high(M, h, v, 1, 10, 0)  # снова избегаем /0
                v = velocity(M, v, 1, 10, 0)  # топливо не выбрасывается в течении 10 секунд
                arr_t.append(arr_t[len(arr_t) - 1] + 10)  # добавляем 10 к времени
            arr_h.append(max(h, 0))  #независимо от перегрузки выводим
            arr_v.append(v)  #
            print("Текущая высота", max(h, 0))  #
            print("Текущая скорость", v)  #
            print("Запас топлива", m0_fluel)  #
        else: #топливо закончилось
            print("Закончилось топливо")
            while h>0: #пока лунолёт не упал, смотрим за его полётом посекундно
                h = high(M,h, v, 1, 1,0)
                v = velocity(M,v, 1, 1,0)
                arr_h.append(max(h,0)) #чтобы не уйти ниже поверхности
                arr_v.append(v)
                arr_t.append(arr_t[len(arr_t)-1]+1)
        if arr_h[len(arr_h)-1]==0:#если же его высота =0
            if abs(v)<=5: print("Победа")#проверка на скорость прилунения
            else: print("Поражение")
            fig=plt.figure()#первый график
            fig.suptitle('Как менялась высота')
            ax = fig.add_subplot(111)
            l = ax.plot(arr_t, arr_h, 'k--')
            plt.show()

            fig = plt.figure()#второй график
            fig.suptitle('Как менялась скорость')
            ax = fig.add_subplot(111)
            l = ax.plot(arr_t, arr_v, 'k--')
            plt.show()
            return 0
    return 0

if __name__ == '__main__':
    main(m0_fluel, u)
