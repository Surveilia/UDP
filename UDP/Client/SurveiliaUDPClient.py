#------------------------------------------
#Program:   SurveiliaUDPClient.py
#Author:    Ben Kennedy
#Last Edit: 2021-11-27
#------------------------------------------

#Required imports
from picamera.array import PiRGBArray
from picamera import PiCamera
from socket import *
from board import *
from Packet import *
import adafruit_dht
import time
import cv2
import imutils
import numpy as np
import argparse
import socket
import sys
import datetime
import os
import smbus2


#GPIO 4 Pin
sensorPin = D4
dht11 = adafruit_dht.DHT11(sensorPin, use_pulseio=False)

#Call instance of packet class
dataPacket = SurveiliaPacket()

#MPU6050 registers and adresses
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

# SMBus variable
bus = smbus2.SMBus(1)

# MPU6050 device adress
deviceAddress = 0x68

# Sensitivity values for MPU6050 board data acquisition
accelSensVal = 16384
gyroSensVal = 131

def MPU_init():
    # Write to sample rate register
    bus.write_byte_data(deviceAddress, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(deviceAddress, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(deviceAddress, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(deviceAddress, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(deviceAddress, INT_ENABLE, 1)


def readRawData(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(deviceAddress, addr)
    low = bus.read_byte_data(deviceAddress, addr+1)

    # Concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536

    return value


# Function for DHT11 sampling
def checkDHT11():

    # Attempt to sample 10 times
    for i in range(10):
        try:
            dht11.measure()
            temp = dht11.temperature
            humid = dht11.humidity

        # If the samples are bad, set the data to 0
        except RuntimeError:
            temp = 0
            humid = 0

        # Return temperature and humidity values
        return [temp, humid]

# Function for taking frames, processing them, and sending them
# to out ground station to be displayed
def detect(frame):

    # Host PC's IPv4 adress and communication port
    UDP_IP = "10.0.0.78"
    UDP_PORT = 5555
    addr = (UDP_IP, UDP_PORT)

    # Buffer value for sending multiple packets
    buffer = 1024

    # Initialize the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   # This receives a frame from the camera and then checks the frame for people.
   # It does this using a histrogram of oriented gradient (HOG) descriptor algorithm to process
   # the image and then usesa pre-trained model (support vector machine or SVM) to check for people.
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride = (4,4), padding = (8,8), scale = 1.03)
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1

    # Puts text regarding detection status on the frame
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)

    # If the person count is one or greater
    if(person>0):

        # Name the file the date and time
        dateTime = str(datetime.datetime.now())
        file_name = (dateTime + ".jpg")

        # Replace characters that are problematic for file transmission
        file_name = file_name.replace('-',' ')
        file_name = file_name.replace(':','_')
        file_name = file_name.replace('.','_',1)

        # Create the jpg image of the frame and set it to be data
        data = cv2.imwrite(file_name, frame)

        # Encode string as bytes for transmission
        bytes = file_name.encode('utf-8')

        # Send file
        print("Sending: ", file_name)
        sock.sendto(bytes, addr)

        # f is the selected file; data is whatever is left that needs to be sent
        f = open(file_name, "rb")
        data = f.read(buffer)

        # Because the UDP packets can store a max of 64KB of data
        # we must send the image using multiple trips
        while(data):
            if(sock.sendto(data,addr)):
               print("Sending Image Packet")
               data = f.read(buffer)

        #Close File
        f.close()

    time.sleep(0.5)

    # Get DHT11 temperature and humidity values
    dht11Data = checkDHT11()
    temp = dht11Data[0]
    humid = dht11Data[1]

    # Round accel data to 3 decimal places
    aX = round((readRawData(ACCEL_XOUT_H) / accelSensVal), 3)
    aY = round((readRawData(ACCEL_YOUT_H) / accelSensVal), 3)
    aZ = round((readRawData(ACCEL_ZOUT_H) / accelSensVal), 3)

    # Round gyro data to 3 decimal places
    gX = round((readRawData(GYRO_XOUT_H) / gyroSensVal), 3)
    gY = round((readRawData(GYRO_YOUT_H) / gyroSensVal), 3)
    gZ = round((readRawData(GYRO_ZOUT_H) / gyroSensVal), 3)

    # Collect all accel/gyro data values in list
    accelData = [aX, aY, aZ]
    gyroData = [gX, gY, gZ]

    # Find sum of accel data for checkSum
    for i in range(len(accelData)):
        accelSum = accelData[i]

    # Find sum of gyro data for checkSum
    for i in range(len(gyroData)):
        gyroSum = gyroData[i]

    # Prepare person count for transmission
    person -= 1

    # Send a flag in packet if a person is detected in frame; Else, don't
    if(person>0):
        flag = 1
    else:
        flag = 0

    # Get checkSum by summing packet data values
    checkSum = (
                   flag
                 + person
                 + temp
                 + humid
                 + accelSum
                 + gyroSum
               )

    # Update the packet with the new values and store it (NEEDS UPDATE)
    dataPacket.updatePacket(checkSum, flag, person, humid, temp, 100, 200)
    storePacket(dataPacket)

    # Send data txt file along with the previously sent frame
    file_name = file_name.replace(".jpg",".txt")

    # Rename txt file written by packet to match frame name
    os.rename("Packet.txt", file_name)

    # Encode the data for transmission
    bytes = file_name.encode('utf-8')

    # Transmit the data to our server
    print("Sending: " + file_name)
    sock.sendto(bytes, addr)

    # Open the txt file for reading in binary format
    # Set the file's contents to the data variable
    file = open(file_name, "rb")
    data = file.read(buffer)

    # While there is data left to send, send it
    while(data):
        if sock.sendto(data, addr):
            print("Sending Data Packet")
            data = file.read(buffer)

    # Close socket and file
    sock.close
    file.close

    # Required delay (increase for slower packet rate)
    time.sleep(0.5)

    # Returns the frame with any detected persons bound by a rectangle
    # The frame is also returned including the total person count and SVM's confidence value
    return frame


# This function is required for capturing frames from the PiCamera
def detectByCamera():

    # Initializes the camera
    camera = PiCamera()
    camera.resolution = (640, 480)
    rawCapture = PiRGBArray(camera, size=(camera.resolution))

    # Tells the camera to capture video continously while storing the current frame
    # From the array into the image variable. It does this by grabbing the raw NumPy array
    # Representing the image, and then initalizing the timestamp
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        # Check the current frame for persons
        detect(image)

        # Clear stream for next frame
        rawCapture.truncate(0)

        # Halt program if the 'q' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

# Main program
if __name__ == "__main__":

    # Calls the pre-trained model for human detection
    # Feed our SVM with it
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Initialize MPU6050 board for data acquisition
    MPU_init()

    # Start video feed
    detectByCamera()
