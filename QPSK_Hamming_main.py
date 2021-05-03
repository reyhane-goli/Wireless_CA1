from transmitter import Transmitter
from  receiver import Receiver
from wireless_channel import wireless_channel
from generate_data import generate_data
import math
import numpy as np
from itertools import chain

class wireless_system:
    def __init__(self, numOfInputs):
        self.transmitter = Transmitter()
        self.receiver = Receiver()
        self.wirelessChannel = wireless_channel(0.1)
        self.numOfInputs = numOfInputs
        self.sigmaValues = [10, 1, 0.1]
        self.generated_Points = []
        self.colors = ['purple', 'yellow', 'orange']

    def runForScatterPlot(self):
        d1 = generate_data() 
        for i in range(len(self.sigmaValues)):
            self.generated_Points = []
            input = open("input.txt", "r")
            AWGNsigma = self.sigmaValues[i]
            self.wirelessChannel.setSigma(AWGNsigma)
            for line in input:
                data = line.rstrip()
                point = self.transmitter.modulate(data)
                (hI, hQ) = self.wirelessChannel.applyChannelGain(point)
                self.wirelessChannel.applyAWGN(point)
                self.generated_Points.append(point)

            d1.showScatterPlot(self.generated_Points ,1/AWGNsigma, self.colors[i])
            input.close()

    def runForLinePlot(self):
        d = generate_data() 
        probabilities = []
        for i in range(1, 100, 1):
            input = open("input.txt", "r")
            numOfCorrectOutputs = 0
            SNR = i
            self.wirelessChannel.setSigma(1/SNR)
            for line in input:
                data = line.rstrip()
                point = self.transmitter.modulate(data)
                (hI, hQ) = self.wirelessChannel.applyChannelGain(point)
                self.wirelessChannel.applyAWGN(point)
                self.receiver.removeChannelImpact(point, hI*0.707, hQ*0.707)
                receiverOut = self.receiver.demodulate(point)
                if(data == receiverOut):
                    numOfCorrectOutputs += 1
            probabilities.append(1 - (numOfCorrectOutputs/self.numOfInputs))
            input.close()

        d.probVsSNR([(i) for i in range(1, 100, 1)], probabilities)

    def encodeAllWithHamming(self):
        input = open("input.txt", "r") 
        output = open("encoded.txt", "w")
        cntr = 0
        for line in input: 
            if(cntr == 0):
                data = line.rstrip()
                cntr +=1
                continue
            else:
                data += line.rstrip()
                cntr = 0
                new_data=" ".join(data)
                data_matrix= np.matrix(new_data)
                encoded = self.transmitter.encodeHamming(data_matrix)
                mystring1= "".join("".join(map(str,sub)) for sub in encoded)
                mystring1 = mystring1.replace('[' , '')
                mystring1 = mystring1.replace(']' , '')
                mystring2="".join(mystring1)
                mystring2 = mystring2.replace(' ' , '')
                output.write((mystring2))

        input.close()
        output.close()



    def runWithHammingCode(self):
        d3 = generate_data() 
        probabilities = []
        self.encodeAllWithHamming()
        for i in range(1, 100, 1):
            allDemodulated = open('demodulated.txt', 'w')
            SNR = i
            self.wirelessChannel.setSigma(1/SNR)
            content_file = open('encoded.txt', 'r')
            content = content_file.read()
            for data in [content[i:i+2] for i in range(0, len(content), 2)] :
                point = self.transmitter.modulate(data)
                (hI, hQ) = self.wirelessChannel.applyChannelGain(point)
                self.wirelessChannel.applyAWGN(point)
                self.receiver.removeChannelImpact(point, hI*0.707, hQ*0.707)
                receiverOut = self.receiver.demodulate(point)
                allDemodulated.write(receiverOut)

            allDemodulated.close()

            self.decodeAll()
            numOfCorrectOutputs = self.reconstructAndCalcCorrectOutputs()
            probabilities.append(1 - (numOfCorrectOutputs/(self.numOfInputs)))

        d3.probVsSNR([i for i in range(1, 100, 1)], probabilities)



    def reconstructAndCalcCorrectOutputs(self):
        numOfCorrects = 0
        counter = 0
        decodedFile = open('decoded.txt', 'r')
        lines = tuple(open('input.txt', 'r'))
        content = decodedFile.read()
        for line in [content[i:i+7] for i in range(0, len(content), 7)] :
            actualData = line[0 : 4]
            parity = line[4:7]
            inputLine1 =str(lines[counter].rstrip())
            inputLine2 = str(lines[counter + 1].rstrip())
            correctedOutput = self.receiver.findAndCorrectError(parity, actualData)
            if(str(correctedOutput[0 : 2]) == inputLine1):
                numOfCorrects += 1
            if(str(correctedOutput[2 : 4] == inputLine2)):
                numOfCorrects += 1
            counter += 2

        return numOfCorrects

    def decodeAll(self):
        demod = open('demodulated.txt', 'r')
        decodedFile = open("decoded.txt", "w")
        lines = demod.read()
        for data in [lines[i:i+7] for i in range(0, len(lines), 7)] :
            new_data=" ".join(data)
            data_matrix= np.matrix(new_data)
            decoded = self.receiver.decodeHamming(data_matrix)
            actualData = data[0:4]
            mystring= "".join("".join(map(str,sub)) for sub in decoded)
            mystring1=str(mystring)
            decodedFile.write(actualData + mystring1)

        demod.close()
        decodedFile.close()

    def runForScatterPlotHamming(self):
        d = generate_data() 
        probabilities = []
        self.generated_Points = []
        for i in range(len(self.sigmaValues)):
            AWGNsigma = self.sigmaValues[i]
            self.wirelessChannel.setSigma(AWGNsigma)
            content_file1 = open('encoded.txt', 'r')
            content = content_file1.read()
            for data in [content[x:x+2] for x in range(0, len(content), 2)] :
                point = self.transmitter.modulate(data)
                (hI, hQ) = self.wirelessChannel.applyChannelGain(point)
                self.wirelessChannel.applyAWGN(point)
                self.generated_Points.append(point)

            d.showScatterPlot(self.generated_Points , 1/AWGNsigma, self.colors[i])
        content_file1.close()

 
def main() :
    w = wireless_system(10000)

    w.runForScatterPlot()
    w.runForLinePlot()

    w.runWithHammingCode()
    

        

if __name__== "__main__":
    main()