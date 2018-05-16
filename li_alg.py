import matplotlib.pyplot as plt
from copy import deepcopy

def read_init(file_name): # чтение поля
    with open(file_name, 'r') as f:
        field_size = list(map(int, f.readline().split()[1::])) # размеры поля
        start = list(map(int, f.readline().split()[1::])) # координаты стартовой клетки
        finish = list(map(int, f.readline().split()[1::])) # координаты финишной
        n = int(f.readline().split()[1]) # количество одиночных препятствий
        walls = []
        for i in range(n):
            walls.append(list(map(int, f.readline().split()))) # считывание препятствий
    return field_size, start, finish, walls


def field_init(field, walls): # проинициализируем пустой словарь
    return {(i, j): [] for i in range(field[0]) for j in range(field[1]) if (i, j) not in walls}


def around(size, around_point, wall): # функция возвращает соседей, если они не стенки
    rd = []
    point = [around_point[0]+1, around_point[1]]
    if 0 < point[0] < size[0] and 0 < point[1] < size[1] and not(point in wall):
        rd.append(point)
    point = [around_point[0]-1, around_point[1]]
    if 0 < point[0] < size[0] and 0 < point[1] < size[1] and not(point in wall):
        rd.append(point)
    point = [around_point[0], around_point[1] - 1]
    if 0 < point[0] < size[0] and 0 < point[1] < size[1] and not(point in wall):
        rd.append(point)
    point = [around_point[0], around_point[1] + 1]
    if 0 < point[0] < size[0] and 0 < point[1] < size[1] and not(point in wall):
        rd.append(point)
    return rd


def go_wide(field_size, field, start, finish, walls): # обход в ширину
    field[tuple(start)] = [0, 'orange'] # будем хранить отдалённость от старта и цвет
    counter = 1 # переменная расстояния от старта
    arounds = [[i, counter] for i in around(field_size, start, walls)] # инициализация соседей с расстояниями
    prev = deepcopy(arounds) # изменяется ли что-то на следующем шаге
    while arounds: # пока не пусто продолжаем
        i, j = arounds.pop(0)
        counter = j + 1
        field[tuple(i)] = [min(field[tuple(i)][0], j) if field[tuple(i)] else j, 'white'] # отметились в точке
        arounds += [[i, counter] for i in around(field_size, i, walls) if field[tuple(i)] == []] # взяли её неотмеченных соседей
        if prev == arounds or arounds == []: # закончились или не изменились
            if field[tuple(finish)]:
                field[tuple(f)][1] = 'orange' # добавили цвет финишной клеточке, если её достигли
            else:
                print("I couldn't")
            return field
        prev = deepcopy(arounds)


def get_way(field_size, field_numered, start, finish, wall): # обход в глубину обратно, зная, что мы с первого раза дойдём до старта
    current_point = finish # идём с финиша
    k = field_numered[tuple(finish)][0] # расстояние
    way = [] # храним путь
    while k != 0:
        # переходим к любой ближайщей к старту клетке
        current_point = [i for i in around(field_size, current_point, wall) if field_numered[tuple(i)][0] == k - 1][0]
        k -= 1 # стали ближе
        way.append(current_point) # записали шаг
    return way


def show_field(field_size, field, walls):
    for i in walls: # рисуем стены
        plt.scatter(i[0], i[1], marker='s', s=field_size[0]*field_size[1], color='black')
    for i, j in field.items(): # рисуем посещённые точки
        plt.text(i[0], i[1], str(j[0]) if j != [] else '')
        if len(j) == 2 and j[1] != 'white':
            plt.scatter(i[0], i[1], marker='s', s=field_size[0] * field_size[1], color=j[1]) # красим посещённые точки жёлтеньким
    plt.xlim(0, field_size[0]) # рисуем всё поле
    plt.ylim(0, field_size[1])
    plt.grid() # сеточка
    # plt.show() # для показа сразу картинки
    plt.savefig('fig.png') # сохранить


if __name__ == '__main__':
    field_size, st, f, w = read_init('input1.txt') # считали
    field = field_init(field_size, w)
    ways_field = go_wide(field_size, field, st, f, w) # пронумеровали
    for i in get_way(field_size, field, st, f, w): # нашли путь
        field[tuple(i)][1] = 'yellow' # покрасили
    show_field(field_size, ways_field, w) # нарисовали