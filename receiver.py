import numpy
from point import point
import numpy as np
import math

class Receiver:

    def __init__(self):

        self.h_matrix = numpy.array([[1, 1, 0, 1, 1, 0, 0],[1, 0, 1, 1, 0, 1, 0],[0, 1, 1, 1, 0, 0, 1]])
        self.regionpoints = {
            "1" : [point(1/math.sqrt(10), 1/math.sqrt(10)), point(1/math.sqrt(10), 3/math.sqrt(10)), point(3/math.sqrt(10), 1/math.sqrt(10)), point(3/math.sqrt(10), 3/math.sqrt(10))],
            "2" : [point(1/math.sqrt(10), -1/math.sqrt(10)), point(1/math.sqrt(10), -3/math.sqrt(10)), point(3/math.sqrt(10), -1/math.sqrt(10)), point(3/math.sqrt(10), -3/math.sqrt(10))],
            "3" : [point(-1/math.sqrt(10), 1/math.sqrt(10)), point(-1/math.sqrt(10), 3/math.sqrt(10)), point(-3/math.sqrt(10), 1/math.sqrt(10)), point(-3/math.sqrt(10), 3/math.sqrt(10))],
            "4" : [point(-1/math.sqrt(10), -1/math.sqrt(10)), point(-1/math.sqrt(10), -3/math.sqrt(10)), point(-3/math.sqrt(10), -1/math.sqrt(10)), point(-3/math.sqrt(10), -3/math.sqrt(10))]
        }

    def demodulate(self, point):
        if(point.getReal() > 0):
            if(point.getImaginary() > 0):
                return "00"
            else:
                return "10"
        else:
            if(point.getImaginary() > 0):
                return "01"
            else:
                return "11"
    
    def removeChannelImpact(self,point, hI , hQ ):
        point.multiply(hI, -hQ)
        return point

    def decodeHamming(self, message):
        message1= np.array(message).T
        dec = numpy.dot(self.h_matrix, message1)%2
        return dec

    
    def findAndCorrectError(self, syndromes, actualData):
        if(syndromes == '000'): # 0 number of errors
            return actualData
        elif(syndromes == '001'): # error in p3
            return actualData
        elif(syndromes == '010'): # error in p2
            return actualData
        elif(syndromes == '011'): # error in d3
            return self.flip(actualData, 2)
        elif(syndromes == '100'): # error in p1
            return actualData
        elif( syndromes == '101'): # error in d2
            return self.flip(actualData, 1)
        elif(syndromes == '110'): # error in d1
            return self.flip(actualData, 0)
        elif(syndromes == '111'): # error in d4
            return self.flip(actualData, 3)
            
    '''def flip(self, string, index):
        returnstr = ""
        for i in range(0, len(string)):
            if(i == 2):
                if(string[i] == "0"):
                    returnstr += "1"
                else:
                    returnstr += "0"
            else:
                returnstr += string[i]

        return returnstr'''

    def flip(self, string, index):
        temp_str=""
        if(string[index]=='0'):
            for i in range(0,len(string)):
                if(i==index):
                    temp_str=temp_str+"1"
                else:
                    temp_str=temp_str+string[i]
            return temp_str
        if(string[index]=='1'):
            for i in range(0,len(string)):
                if(i==index):
                    temp_str=temp_str+"0"
                else:
                    temp_str=temp_str+string[i]
            return temp_str

    def demodulate16(self, point):
        if(point.getReal() > 0):
            if(point.getImaginary() > 0):
                nearestIdx = point.findNearest(self.regionpoints.get("1"))
                return("{0:b}".format(nearestIdx).zfill(4))
            else:
                nearestIdx = point.findNearest(self.regionpoints.get("4"))
                return("{0:b}".format(nearestIdx + 4).zfill(4))
        else :
            if(point.getImaginary() > 0):
                nearestIdx = point.findNearest(self.regionpoints.get("2"))
                return("{0:b}".format(nearestIdx + 8).zfill(4))
            else:
                nearestIdx = point.findNearest(self.regionpoints.get("3"))
                return("{0:b}".format(nearestIdx + 12).zfill(4))