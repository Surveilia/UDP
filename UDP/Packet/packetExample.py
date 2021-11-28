import Packet

# Description:    Example of basic usage for the Packet designed for Surveilia. Stores data to a file named "Packet.txt"

# Written By:     Chase Westlake

# Packet contains in order: 7 items
                # - Check sum
                # - personFlag
                # - # of people
                # - humidity
                # - Temp
                # - accelerometer
                # - gyroscope

# Initialiaze packet with handle. 
packet = Packet.SurveiliaPacket()

# Update packet with values. These values are arbitrary, fill with needed packet data
packet.updatePacket(1,2,3,4,5,6,7)
