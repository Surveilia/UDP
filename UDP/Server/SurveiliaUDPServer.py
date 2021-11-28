#------------------------------------------
#Program:   SurveiliaUDPServer.py
#Author:    Ben Kennedy
#Last Edit: 2021-11-27
#------------------------------------------

# Required Imports
from socket import *
import os.path

# Infinite Loop
while (True):

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

    # Get a string version of the received bytes-like data
    dataString = str(data.strip())

    # Find the last character in the data
    lastChar = dataString[-2]

    # If the last character is a t (.txt), we know it's a data packet
    if lastChar == 't':
        savePath = 'C:/Surveilia/UDP/Data/'

    # If the last character is a g (.jpg), we know it's a image packet
    elif lastChar == 'g':
        savePath = 'C:/Surveilia/UDP/Image/'

    # If it isn't either of those, we can assume it's a corrupted/bad packet
    else:
        savePath = 'C:/Surveilia/UDP/Quarantine'

    # Decodes data, adds correct file path, re-encodes data
    decodedData = data.strip().decode("utf-8")
    decodedDataWithPath = os.path.join(savePath, decodedData)
    encodedData = decodedDataWithPath.encode("utf-8")

    # Display the file name as well as the file path
    print("Downloading:   ", encodedData)

    # Open the file for writing in binary mode
    file = open(encodedData, 'wb')

    # Receives data from the socket using the buffer
    data, addr = sock.recvfrom(buffer)

    try:
        # While there is more packets to come
        while (data):
            # Keep writing the data to the file until it's done (1ms intervals between packets of the same data)
            file.write(data)
            sock.settimeout(1)
            data, addr = sock.recvfrom(buffer)

    except timeout:
        # File downloaded; restart program
        print("File Downloaded")
        file.close()
