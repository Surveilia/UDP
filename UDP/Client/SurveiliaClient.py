#------------------------------------------
#Program: humanDetection_UDPFileTransfer.py
#Author:  Ben Kennedy
#Date:    2021-10-28
#------------------------------------------

# Required imports
from picamera.array import PiRGBArray
from picamera import PiCamera
from socket import *
import time
import cv2
import imutils
import numpy as np
import argparse
import socket
import sys
import datetime
def detect(frame):

    # Relevant socket variables
    UDP_IP = "10.0.0.78"
    UDP_PORT = 5555
    buffer = 1024
    addr = (UDP_IP,UDP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

   #This receives a frame from the camera and then checks the frame for people.
   #It does this using a histrogram of oriented gradient (HOG) descriptor algorithm to process
   #the image and then usesa pre-trained model (support vector machine or SVM) to check for people.
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
    if(person>=1):

        # Name the file the date and time
        dateTime = str(datetime.datetime.now())
        file_name = (dateTime + ".jpg")

        # Replace characters that are problematic for file transmission
        file_nameTransmittable = file_name.replace('-',' ')
        file_nameTransmittable = file_nameTransmittable.replace(':','_')
        file_nameTransmittable = file_nameTransmittable.replace('.','_',1)

        # Create the jpg image of the frame and set it to be data
        data = cv2.imwrite(file_nameTransmittable, frame)

        # Encode string as bytes for transmission
        bytes = file_nameTransmittable.encode('utf-8')

        # Send file
        print("Sending: ", file_nameTransmittable)
        sock.sendto(bytes, addr)

        # f is the selected file; data is whatever is left that needs to be sent
        f = open(file_nameTransmittable, "rb")
        data = f.read(buffer)

        # Because the UDP packets can store a max of 64KB of data
        # we must send the image using multiple trips
        while(data):
            if(sock.sendto(data,addr)):
               print("...")
               data = f.read(buffer)

        # socket/file close
        sock.close()
        f.close()

    # Delay for 2 seconds (increase this for slower image rate)
    time.sleep(2)

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

    # Start video feed
    detectByCamera()
