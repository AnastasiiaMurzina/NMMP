import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as axes3d
import copy

class Cell:
    N=10**3
    L=int(N**(1/3.))+1
    dt=0.0000001
    distr=[]
    distr_n=[]
    distr_a=[]
    distr_potencial=[]

    def __init__(self):
        self.init_dist()
        self.init_potencial()
        # self.init_a()
    #
    def potencial(self,x):
        if x<=1:
            return np.inf
        else:
            return -x**(-6)
        # return x**12-0.5*x**6

    def interaction(self,i,j):
        if i==j:
            return [0,0,0]
        r=(self.distr_n[i]-self.distr_n[j])%(self.L)
        d=float(r[0]**2+r[1]**2+r[2]**2)
        # print(d)
        return (((self.potencial(d))*6*d**(-2))*np.array(r))

    def init_dist(self):
        eps=0.05

        for i in range(int(self.L)):
            for j in range(int(self.L)):
                for k in range(int(self.L)):
                    self.distr.append([i*(1+eps),j*(1+eps),k*(1+eps)])
                    self.distr_n.append([i*(1+eps),j*(1+eps),k*(1+eps)])
        self.distr=np.array(self.distr)
        self.distr_n=np.array(self.distr_n)
        self.L += eps * self.L

    def init_a(self):
        for i in range(self.N):
            count=np.array([0.,0.,0.])
            for j in range(self.N):
                if j!=i:
                    count+=self.interaction(i,j)
            self.distr_a.append(count)
        self.distr_a=np.array(self.distr_a)
        return self.distr_a

    def plot_3d(self):
        fig = plt.figure(dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        fx = [index[0] for index in ((self.distr_n))]
        fy = [index[1] for index in ((self.distr_n))]
        fz = [index[2] for index in ((self.distr_n))]

        ax.scatter(fx, fy, fz)
        ax.set_xlim3d(0, self.L)
        ax.set_ylim3d(0., self.L)
        ax.set_zlim3d(0., self.L)
        plt.show()

    def set_distr_a(self):
        for i in range(self.N):
            count=np.array([0.,0.,0.])
            for j in range(self.N):
                if j!=i:
                    count+=self.interaction(i,j)
            self.distr_a[i]=(count)
        return self.distr_a

    def leap_frog(self):
        array = copy.deepcopy(self.distr)
        self.distr = self.distr_n
        # print(type(self.L))
        print(self.dt**2*self.distr_a)

        self.distr_n=(2*self.distr-array + self.dt**2*self.distr_a)%self.L
        return self.distr_n

    def init_potencial(self):
        for i in range(self.N):
            count=np.array([0.,0.,0.])
            for j in range(self.N):
                if j!=i:
                    count+=self.interaction(i,j)
            self.distr_potencial.append(count)
        self.distr_potencial=np.array(self.distr_potencial)
        return self.distr_potencial
def main():
    my_cell = Cell()
    # range_interaction=my_cell.L
    print(my_cell.distr_potencial)
    # my_cell.plot_3d()
    # print ("I have gone to count the interaction")
    # for i in range(10):
    #     my_cell.leap_frog()
    # print(my_cell.distr_n)
    # my_cell.plot_3d()

if __name__ == '__main__':
    main()
