from random import randint
import matplotlib.pyplot as plt
import numpy as np
import math
from point import point

class generate_data :

    def generateQpskData(self):
        f = open("input.txt", "w")
        for i in range(0, 10000):
            a0 = (randint(0, 1))
            a1 = (randint(0, 1))
            f.write((str(a0) + str(a1))+"\n")
        f.close()

    def generateQamData(self):
        f = open("input4.txt", "w")
        for i in range(0, 10000):
            a0 = (randint(0, 1))
            a1 = (randint(0, 1))
            a2 = (randint(0, 1))
            a3 = (randint(0, 1))
            f.write((str(a0) + str(a1) + str(a2) + str(a3))+"\n")
        f.close()

    def showScatterPlot(self, predicted, SNR, color):
        fig, ax = plt.subplots()
        data1=[]
        data2= []
        for i in range(len(predicted)):
            data1.append(predicted[i].getReal())
            data2.append(predicted[i].getImaginary())

        points = [point(0.707, 0.707), point(-0.707, 0.707), point(0.707, -0.707), point(-0.707, -0.707)]

        ax.scatter(data1, data2, c = color, s = 10.)
        for i  in range(0, len(points)):
            p = points[i]
            ax.scatter(p.getReal(), p.getImaginary() ,c = 'cyan', s = 10.)

        ax.set_xlabel('I', fontsize=15)
        ax.set_ylabel('Q', fontsize=15)
        ax.set_title('Received signal for SNR= '+str(SNR))

        ax.grid(True)
        fig.tight_layout()
        plt.show()

    def probVsSNR(self, x, y):
        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.set(xlabel='SNR', ylabel='Probability',
        title='Probability VS SNR')
        ax.grid()

        fig.savefig("test.png")
        plt.show()


def main():
    d = generate_data()
    d.generateQpskData()
    #d.generateQamData()

if __name__ == "__main__":
    main()