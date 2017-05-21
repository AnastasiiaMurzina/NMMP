import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

pause = False
f=open(sys.argv[1],'r') #первым параметром считываем с консоли файл с начальным распределением
total_time = int(sys.argv[2]) #втором - время игры
color='summer' #цвет по-умолчанию
try:
    f1=open(sys.argv[3],'r') #если третий парметр есть и такой файл надайден, то
    color = f1.readline() #считываем название цветовой гаммы
    f1.close()
except FileNotFoundError: print("Файл не найден, поэтому использую свои цвета")
except IndexError: print("Файл не указан, поэтому использую свои цвета")

N, M = f.readline().split()
N, M = [int(N), int(M)] #считываем размер поля и преобразовываем его к int
grid = np.zeros((N,M)) #массив из нулей
ON = 255
OFF = 0
vals = [ON, OFF]

for i in range(N): #записываем массив из файла
    line = f.readline().split()
    for j in range(M):
        if line[j] == '0': grid[i][j]=OFF
        else: grid[i][j]=ON
f.close()
n=0 #временной счётчик
fig = plt.figure()
cmap = mpl.cm.get_cmap('gnuplot')
ax = fig.add_subplot(111)
# вызываем метод pcolor. Вводим пользовательскую раскраску через cmap
cs = ax.pcolor(grid, cmap=cmap)
ax.set_title(u'Начальное распределние, в живых %d' %np.count_nonzero(grid == ON))
plt.show()
# plt.savefig('init.png')
while n!=total_time:
  newGrid = grid.copy() #глубокое копирование для нового состояния
  for i in range(N): #для каждой клетки провериям выполнения условий
    for j in range(M):
      #учитываем все 8 соседей (остаток от деления % используем для тороидальных граничных условий)
      total = (grid[i, (j-1)%M] + grid[i, (j+1)%M] +
               grid[(i-1)%N, j] + grid[(i+1)%N, j] +
               grid[(i-1)%N, (j-1)%M] + grid[(i-1)%M, (j+1)%M] +
               grid[(i+1)%N, (j-1)%M] + grid[(i+1)%M, (j+1)%M])/255
      # если сама клетка была живой
      if grid[i, j]  == ON:
        if (total < 2) or (total > 3): #число соседей не равно 2 или 3
          newGrid[i, j] = OFF #тогда она умирает
      else:#если он была мёртвой
        if total == 3:#то ей нужно 3 живых соседа, чтобы стать живой
          newGrid[i, j] = ON#иначе не меняем её состояние
  grid=newGrid.copy()
  n+=1 #увеличиваем счётчик
  fig = plt.figure()
  ax = fig.add_subplot(111)
  cs = ax.pcolor(grid, cmap=cmap)

  ax.set_title(u'Время %d, в живых %d' %(n, np.count_nonzero(grid == ON)))
  plt.show()
  # plt.savefig('it_%d.png' %n)

