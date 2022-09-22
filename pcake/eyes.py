# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os.path
import os

# %%
INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS = 100
eyes_output_path = 'static/lasteyes.txt'
face_path = 'faces'
lasteyes = datetime.datetime.now() - datetime.timedelta(days=1)
timestamp = lambda: datetime.datetime.now().isoformat().replace(":","_").replace(".", "_")

if not os.path.isdir(face_path):
    os.makedirs(face_path)

# face_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# dump some images
print(f'{timestamp()}: dump 100 frames')
for _ in range(100):
    _, img = cap.read()

print(f'{timestamp()}: start real capture')
try:
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imwrite('static/cur.png', img)
        if len(faces) > 0:
            print(f'{timestamp()}: eyes detected')
            with open(eyes_output_path, 'w') as f:
                f.write(datetime.datetime.now().isoformat())
            if (datetime.datetime.now() - lasteyes).total_seconds() > INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS:
                print(f'{timestamp()}: those are new eyes, save to faces')
                cv2.imwrite(os.path.join(face_path, f'{timestamp()}.png'), img)
                lasteyes = datetime.datetime.now()
finally:
    cap.release()

# %%
