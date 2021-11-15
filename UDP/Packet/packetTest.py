import packetClass
# Packet contains in order:
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope
T1 = packetClass.SurveiliaPacket(10, False, 0, 10, 20, 180, 90)