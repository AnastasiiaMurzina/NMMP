from itertools import combinations
import matplotlib.pyplot as plt

def named_coordinates(file_name):
    '''
    :param file_name: имя файла для считывания координат
    :return: словарь координат, начиная с нулевой
    '''
    d = {}
    with open(file_name, 'r') as f:
        i = 0
        for line in f:
            d.update({i: list(map(float, line.split()))})
            i += 1
    return d


def distances(coords):
    '''
    :param coords: словарь координат
    :return: словарь всевозможных расстояний
    '''
    diss = {}
    for i in combinations(coords, 2): #выбираем все пары точек и считаем расстояния между ними
        diss.update({((coords[i[0]][0] - coords[i[1]][0]) ** 2 + (coords[i[0]][1] - coords[i[1]][1]) ** 2) ** 0.5: (i[0], i[1])})
    return diss


def cycle_exists(G):
    marked = {u: False for u in G}  # все узлы изначально не посещены
    found_cycle = [False]  # изначальный флаг цикла
    for u in G:  # - Visit all nodes.
        if not marked[u]:
            dfs_visit(G, u, found_cycle, u, marked)
        if found_cycle[0]:
            break
    return found_cycle[0]


def dfs_visit(G, u, found_cycle, pred_node, marked):
    if found_cycle[0]:  # - остановка при нахождении цикла
        return
    marked[u] = True  # - отмечаем посещение
    for v in G[u]:  # - проходим по соседям
        if marked[v] and v != pred_node:  # - сосед отмечен и мы в него опять попали
            found_cycle[0] = True  # цикл существует
            return
        if not marked[v]:  # рекурсивный вызов обхода
            dfs_visit(G, v, found_cycle, u, marked)


def prim_alg(ds):
    '''
    :param ds: расстояния
    :return: искомый граф
    '''
    G = {i: [] for i in range(n)} # инициализируем граф пустым списком смежности
    count_edges = 0 # число рёбер для остановки сразу после соединения всех точек
    for i in sorted(list(ds.keys())): # идём по расстояниям в сторону увеличения
        G[ds[i][0]].append(ds[i][1]) # добавляем ребро
        G[ds[i][1]].append(ds[i][0])
        if cycle_exists(G): # проверяем наличие цикла
            G[ds[i][0]].pop() # если есть, то удаляем последние добавленные рёбра
            G[ds[i][1]].pop()
        else: # благополучно принимаем ребро
            count_edges += 1
        if count_edges == n - 1: # больше не надо
            break
    return G


def draw(G, coords):
    '''
    :param G:
    :param coords:
    :return: картинка (последняя строка сохраняет 'fig.png' или предыдущая выводит сразу)
    '''
    for i in range(len(G.keys())): # прорисовываем все точки
        plt.scatter(coords[i][0], coords[i][1])
    for i, j in G.items(): # прорисовываем рёбра
        for point in j:
            plt.plot([coords[i][0], coords[point][0]], [coords[i][1], coords[point][1]])
    plt.show()
    # plt.savefig('fig.png')


if __name__ == '__main__':
    coords = named_coordinates('input.txt') # посчитали координаты
    ds = distances(coords) # получили расстояния
    n = len(coords)
    G = prim_alg(ds) # получаем искомые связи
    draw(G, coords) # прорисовываем

