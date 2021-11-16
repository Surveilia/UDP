import Packet
# Packet contains in order:
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope
T1 = Packet.SurveiliaPacket(10, 0, 0, 10, 20, 180, 90)

T1.storePacket()