# pip install opencv-python
import os
import cv2
import time
import emailing
import glob
from threading import Thread

video = cv2.VideoCapture(0) # 0 if you have only one camera, 1 would be secondary camera.
time.sleep(1)  # We give the camera some time to load

first_frame = None
status_list = []
count = 1

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # creating grey frame
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0) # creating blur frame

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame,60 ,255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours: # finding the object (real and the fake object)
        if cv2.contourArea(contour) < 6000: # 5000px
            continue # if it is a fake object we continue
        x, y, w, h = cv2.boundingRect(contour) # drawing rectangle around the object
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)  # Storing the images
            count = count + 1
            all_images = glob.glob("images/*.png") # We want to capture the image in the middle here
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0: # This measns that obejct has just exited the frame
        email_thread = Thread(target=emailing.send_email, args=(image_with_object, )) # THREADING IN PYTHON. FUNTION CALLING EXAMPLE
        email_thread.daemon = True
        clean_thread = Thread(target=emailing.clean_folder)  # after sending out the email we clean the folder
        clean_thread.daemon = True

        email_thread.start() # SEND EMAIL



    cv2.imshow("Video", frame)
    cv2.imshow("My video", dil_frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
clean_thread.start() # DELETE IMAGES
