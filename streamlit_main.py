# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 21:42:12 2025

@author:https://consoleflare.com/blog/streamlit-app-for-qr-toolkit/#:~:text=In%20this%20blog%20post%2C%20we%E2%80%99ll%20introduce%20you%20to,proceeding%20let%20us%20understand%20what%20is%20QR%20first.
"""

import streamlit as st
import pyqrcode
from io import BytesIO
from PIL import Image
import cv2
from pyzbar import pyzbar
import pandas as pd
import datetime
import os

os.chdir(r"C:\Users\User\Documents\qr_reading_writing")
data=pd.read_excel(r"data/Registro_general.ods")
def generate_qr_code(data):
    """
    Generates a QR code image from the provided data.

    Parameters:
    data (str): The data to encode in the QR code.

    Returns:
    BytesIO: The QR code image in a BytesIO buffer.
    """
    qr = pyqrcode.create(data)
    buffer = BytesIO()
    qr.png(buffer, scale=6)
    buffer.seek(0)
    return buffer

def decode_qr_code(frame):
    """
    Decodes QR codes in the given image frame.

    Parameters:
    frame (numpy.ndarray): The image frame to scan for QR codes.

    Returns:
    list: A list of decoded QR code data.
    """
    decoded_objects = pyzbar.decode(frame)
    qr_codes = [obj.data.decode('utf-8') for obj in decoded_objects]
    return qr_codes

def create_qr_code():
    st.title("QR Code Generator")
    data = st.text_input("Enter the data to encode in the QR code")  # input by user

    if data:
        qr_image = generate_qr_code(data)    # function generate_qr_code with data as argument
        img = Image.open(qr_image)

        st.image(img, caption="Generated QR Code", use_column_width=False)

        st.download_button(
            label="Download QR Code",
            data=qr_image,
            file_name="qrcode.png",
            mime="image/png"
        )


def scan_qr_code():
    st.title("QR Code Scanner")
    st.write("Click the button below to start the camera and scan a QR code.")

    # Initialize session state for control buttons and decoded message
    if "scanning" not in st.session_state:
        st.session_state.scanning = False

    if "decoded_message" not in st.session_state:
        st.session_state.decoded_message = None

    def start_scanning():
        st.session_state.scanning = True

    def stop_scanning():
        st.session_state.scanning = False

    if not st.session_state.scanning:
        if st.button('Start Scanning', key='start'):
            start_scanning()

    if st.session_state.scanning:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while st.session_state.scanning:
            ret, frame = cap.read()
            if not ret:
                st.write("Failed to capture image.")
                break

            qr_codes = decode_qr_code(frame)

            # Display the frame
            stframe.image(frame, channels="BGR")

            # Display the decoded QR codes if it's a new message
            if qr_codes:
                
                if st.session_state.decoded_message != qr_codes[0]:
                    st.session_state.decoded_message = qr_codes[0]
                    st.success(f"Decoded QR Code: {qr_codes[0]}")
                    return qr_codes[0]
                    

        if st.button('Stop Scanning', key='stop', on_click=stop_scanning):
            cap.release()
            cv2.destroyAllWindows()
def registrar_llegada(save=True):
    base2=pd.read_excel(r"data/Registro_llegada.ods")
    now = datetime.datetime.now()    
    valores=scan_qr_code()
    print(1)
    datos_particulares=data.loc[data['Identificación'] == int(valores)]
    print(valores)
    datos_particulares["hora_registro"]=str(now)
    if save:
        try:
            datos_particulares.to_csv(r"data/Registro_llegada.txt",mode="a",header=False)
            print(3)
        except Exception as e:
            print(e)                   
    return datos_particulares
    
st.title("QR Code Toolkit")

option = st.radio(
    "Choose an option:",
    ("Create QR", "cargar usuario")
)

if option == "Create QR":
    create_qr_code()
elif option == "cargar usuario":
    registrar_llegada()
