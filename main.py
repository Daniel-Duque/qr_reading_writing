# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 11:14:58 2024

@author: usuario
"""

#used drive ai generation code for this

import cv2
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
        return data
        # Display the resulting frame
        cv2.imshow('QR Code Detector', img)
    
        # Check for key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release video capture and destroy all windows
    vid.release()
    cv2.destroyAllWindows()
