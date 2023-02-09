import streamlit as st
import cv2

st.title("Motion Detector")

button = st.button("Open camera")

if button:
    streamlit_image = st.image([])
    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(img=frame, text="Hello", org=(50, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(28,108,208), thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)