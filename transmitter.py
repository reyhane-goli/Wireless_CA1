from point import point
import numpy
import math
import copy

class Transmitter:

    def __init__(self):
        #generates [d1, d2, d3, d4, p1, p2, p3]
        self.g_matrix =  numpy.array([[1, 0, 0, 0, 1, 1, 0],[0, 1, 0, 0, 1, 0, 1],[0, 0, 1, 0, 0, 1, 1],[0, 0, 0, 1, 1, 1, 1]])
        self.qam16Dict = {
            "0000" : point(1/math.sqrt(10), 1/math.sqrt(10)),
             "0001" : point(1/math.sqrt(10), 3/math.sqrt(10)),
             "0010" : point(3/math.sqrt(10), 1/math.sqrt(10)),
             "0011" :point(3/math.sqrt(10), 3/math.sqrt(10)),
             "0100" :point(1/math.sqrt(10), -1/math.sqrt(10)),
             "0101" :point(1/math.sqrt(10), -3/math.sqrt(10)),
             "0110" :point(3/math.sqrt(10), -1/math.sqrt(10)),
             "0111" :point(3/math.sqrt(10), -3/math.sqrt(10)),
             "1000" :point(-1/math.sqrt(10), 1/math.sqrt(10)),
             "1001" :point(-1/math.sqrt(10), 3/math.sqrt(10)),
             "1010" :point(-3/math.sqrt(10), 1/math.sqrt(10)),
             "1011" :point(-3/math.sqrt(10), 3/math.sqrt(10)),
             "1100" :point(-1/math.sqrt(10), -1/math.sqrt(10)),
             "1101" :point(-1/math.sqrt(10), -3/math.sqrt(10)),
             "1110" :point(-3/math.sqrt(10), -1/math.sqrt(10)),
             "1111" :point(-3/math.sqrt(10), -3/math.sqrt(10))
        }

    def modulate(self, input):
        if(input == "00"):
            return point(0.707, 0.707)
        elif(input == "01"):
            return point(-0.707, 0.707)
        elif(input == "10"):
            return point(0.707, -0.707)
        else :
            return point(-0.707, -0.707)

    def encodeHamming(self, message):
        enc = numpy.dot(message, self.g_matrix)%2
        return enc

    def modulate16QAM(self, input):
        return  copy.deepcopy(self.qam16Dict[input])