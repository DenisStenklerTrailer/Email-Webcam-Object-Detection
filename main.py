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
    thresh_frame = cv2.threshold(delta_frame,10 ,255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours: # finding the object (real and the fake object)
        if cv2.contourArea(contour) < 5000: # 5000px
            continue # if it is a fake object we continue
        x, y, w, h = cv2.boundingRect(contour) # drawing rectangle around the object
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
    cv2.imshow("Video", frame)

    cv2.imshow("My video", dil_frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
