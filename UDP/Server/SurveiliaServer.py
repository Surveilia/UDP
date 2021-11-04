# Required Imports
from socket import *

# Infinite Loop
while(1):
    # UDP/Socket variables
    UDP_IP = "10.0.0.78"
    UDP_PORT = 5555
    addr = (UDP_IP, UDP_PORT)

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((addr))
    buffer = 1024

    # Set the incoming file as data and open the file
    data, addr = sock.recvfrom(buffer)
    print("Received File: ", data.strip())
    file = open(data.strip(), 'wb')

    data, addr = sock.recvfrom(buffer)

    try:
        # While there is more packets to come
        while (data):
            # Keep writing the data to the file until it's done
            file.write(data)
            sock.settimeout(2)
            data, addr = sock.recvfrom(buffer)

    except timeout:
        # File downloaded; restart program
        print("File Downloaded")