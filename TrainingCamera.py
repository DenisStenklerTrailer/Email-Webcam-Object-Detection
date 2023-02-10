import streamlit as st
import cv2
from datetime import datetime


st.title("Motion Detector")

button = st.button("Open camera")

if button:
    streamlit_image = st.image([])
    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        now = datetime.now()
        time = str(now.strftime("%H:%M:%S"))
        date = str(now.strftime("%d/%m/%Y"))

        cv2.putText(img=frame, text=time, org=(50, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(255,255,255), thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=date, org=(50, 100),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(255, 255, 100), thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)