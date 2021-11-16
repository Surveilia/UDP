#   Written by:     Chase Westlake

#   Description:    This class contructs the packet contents to send in UDP

#   Project:        Surveilia

#   How to use:     To use the packet object: 
#                                                         chksum,  personFlag, personCount, humidity(%), Temperature, Accelerometer, Gyroscope      
#                   Packet = packetClass.SurveiliaPacket( 10,      False,      0,           10,          20,          180,           90)

#   In use:         Packet = packetClass.SurveiliaPacket(10, 0, 0, 10, 20, 180, 90)

#   Packet contains in order:
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope
                # - GPS (maybe)

class SurveiliaPacket:
    def __init__(self, chkSum, flag, count, humid, temp, acc, gyro):
        self.checkSum = chkSum
        self.Flag = flag
        self.PersonCount = count
        self.Humidity = humid
        self.Temperature = temp
        self.Accelerometer = acc
        self.Gyroscope = gyro
        
    def setChkSum(self, chkSum):
        self.checkSum = chkSum
    
    def setFlag(self, flag):
        self.Flag = flag
        
    def setPersCt(self, count):
        self.PersonCount = count
        
    def setHumidity(self, humid):
        self.Humidity = humid
        
    def setTemp(self, temp):
        self.Temperature = temp     

    def setAccel(self, acc):
        self.Accelerometer = acc
        
    def setGyro(self, gyro):
        self.Gyroscope = gyro
        
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
