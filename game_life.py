import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

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

def update(data):
  global grid
  global n
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

  mat.set_data(newGrid)#устанавливаем для показа новый массив значений
  grid = newGrid#для следующего шага этот будет предыдущим
  ttl.set_text('время ='+str(n)) #надпись со временем
  cont_life.set_text('в живых ='+str(np.count_nonzero(grid == ON))) #выводим кол-во живых
  n+=1 #увеличиваем счётчик
  return [mat], ttl, cont_life
#настраиваем анимацию
fig, ax = plt.subplots()
mat = ax.matshow(grid, cmap=(color))
ttl = ax.text(-0.3, 1., 'время', transform = ax.transAxes)
cont_life = ax.text(-0.3, 0., 'в живых ', transform = ax.transAxes)
ttl.set_text('')
cont_life.set_text('')
ani = animation.FuncAnimation(fig, update, interval=50,repeat = False)
#не выполнены условия остановки анимации, поэтому при остановке появляется ошибка AttributeError
#сторчка ниже - попытка сохранить запись, но у меня не установлен ffmpeg... так что без понятия как это будет работать
# ani.save('life.mp4', writer='ffmpeg', fps=2, frames = total_time)
plt.show()
