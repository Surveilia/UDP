#   Written by:     Chase Westlake

#   Description:    This class contructs the packet contents to send in UDP

#   Project:        Surveilia

#   How to use:     To use the packet object, example data: 
#                                                         chksum,  personFlag,  personCount, humidity(%), Temperature, Accelerometer, Gyroscope      
#                   Packet = packetClass.SurveiliaPacket( 10,      0 or 1,      0,           10,          20,          180,           90)

#   In use:         Packet = packetClass.SurveiliaPacket()
#                   Packet.updatePacket(fill values with packet content)

#   Header:         import Packet

#   Packet contains in order:
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope
                # - GPS (maybe), not supported


class SurveiliaPacket:
    
    #initializes packet. -1 represents absense of data
    def __init__(self):
        self.checkSum = -1
        self.Flag = -1
        self.PersonCount = -1
        self.Humidity = -1
        self.Temperature = -1
        self.Accelerometer = -1
        self.Gyroscope = -1
        
        # Updates packet with values
    def updatePacket(self, chkSum, flag, count, humid, temp, acc, gyro):
        self.checkSum = chkSum
        self.Flag = flag
        self.PersonCount = count
        self.Humidity = humid
        self.Temperature = temp
        self.Accelerometer = acc
        self.Gyroscope = gyro
        storePacket(self)
        
# Stores current packet on every update
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
