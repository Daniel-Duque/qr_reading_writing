# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 11:14:58 2024

@author: usuario
"""

#used drive ai generation code for this

import cv2
import numpy as np
import qrcode
import os 
import time
import pandas as pd
os.chdir(r"C:\Users\Asistente IBC\Documents\qr\qr_reading_writing-main\qr_reading_writing-main")
data=pd.read_excel(r"data/Registro_llegada.xlsx")

def detect_qr():
    # prompt: give me a code to detect a qr code
    # Initialize video capture
    vid = cv2.VideoCapture(0)
    
    # Initialize QRCode detector
    detector = cv2.QRCodeDetector()
    
    while True:
        # Read frame from video
        _, img = vid.read()
    
        # Detect QR code
        data, bbox, _ = detector.detectAndDecode(img)
    
        # Check if QR code is detected
        if data:
            print(data)
            vid.release()
            return data
        
        # Display the resulting frame
        cv2.imshow('QR Code Detector', img)
    
        # Check for key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    
def generate_qr(text):
    # prompt: give me a code to generate a qr code
    # Release video capture and destroy all windows

    
    # Define the QR code data

    # Initialize the QRCode object
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    # Add the data to the QR code
    qr_code.add_data(text)
    
    # Generate the QR code image
    qr_image = qr_code.make_image(fill_color="black", back_color="white")
    
    qr_image.save(r"images/"+str(text)+".png")

def registrar_llegada():
    valores=detect_qr()
    
    
detect_qr()
generate_qr("255542151")
