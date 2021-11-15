import json
import time
import random

index = 0
data = []

#   Written by:     Chase Westlake

#   Description:    This class contructs the packet contents to send in UDP

#   Project:        Surveilia

#   How to use:     To use the packet object: 
#                                                         chksum,  personFlag, personCount, humidity(%), Temperature, Accelerometer, Gyroscope      
#                   Packet = packetClass.SurveiliaPacket( 10,      False,      0,           10,          20,          180,           90)

#   In use:         Packet = packetClass.SurveiliaPacket(10, False, 0, 10, 20, 180, 90)

#   Packet contains in order:
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope
                # - GPS (maybe)

#file is either the jpg image or the chart
class SurveiliaPacket:
    def __init__(self, chkSum, flag, count, humid, temp, acc, gyro):
        self.checkSum = chkSum
        self.Flag = flag
        self.PersonCount = count
        self.Humidity = humid
        self.Temperature = temp
        self.Accelerometer = acc
        self.Gyroscope = gyro
        storePacket()
        
    def setChkSum(self, chkSum):
        self.checkSum = chkSum
        storePacket(self)
    
    def setFlag(self, flag):
        self.Flag = flag
        storePacket()
        
    def setPersCt(self, count):
        self.PersonCount = count
        storePacket()
        
    def setHumidity(self, humid):
        self.Humidity = humid
        storePacket()
        
    def setTemp(self, temp):
        self.Temperature = temp
        storePacket()
        
    def setAccel(self, acc):
        self.Accelerometer = acc
        storePacket()
        
    def setGyro(self, gyro):
        self.Gyroscope = gyro
        storePacket()
        
    def storePacket(self):

        with open('Packet.txt', 'w') as Packet:
            Packet.write(str(self.checkSum) + '\n')
            Packet.write(str(self.Flag) + '\n')
            Packet.write(str(self.PersonCount) + '\n')
            Packet.write(str(self.Humidity) + '\n')
            Packet.write(str(self.Temperature) + '\n')
            Packet.write(str(self.Accelerometer) + '\n' )
            Packet.write(str(self.Gyroscope) + '\n')
        
                # ::::Packet Structure::::
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope

# for x in range(0,999):
    # data.append(random.randint(0,5000))

# print(data)

# with open('dataTXT.txt', 'w') as outfile:
    # for x in data:
        # index += 1
    # outfile.writelines(str(index) + '\n')
    # for x in data:
        # outfile.writelines(str(x) +'\n')
# print("Data written as text")
# outfile.close()

# dataStore = []

# with open('dataTXT.txt', 'r') as infile:
    # dataStore = infile.readlines()
# dataStore = [Line.strip() for Line in dataStore]
# print("\n")
# print(dataStore)