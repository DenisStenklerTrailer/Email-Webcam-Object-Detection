# pip install opencv-python
import cv2
import time

video = cv2.VideoCapture(0) # 0 if you have only one camera, 1 would be secondary camera.
time.sleep(1)  # We give the camera some time to load

first_frame = None

while True:
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # creating grey frame
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0) # creating blur frame

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("My video", delta_frame)

    cv2.threshold(delta_frame,30 ,255, cv2.THRESH_BINARY)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
