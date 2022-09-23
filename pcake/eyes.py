# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os.path
import os
import requests
import serial
import serial.tools.list_ports

# sudo /home/gumjum/anaconda3/envs/cake/bin/python eyes.py

# %%
INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS = 100
eyes_output_path = 'static/lasteyes.txt'
cake_output_path = 'static/cake.txt'
face_path = 'static/faces'
lasteyes = datetime.datetime.now() - datetime.timedelta(days=1)
timestamp = lambda: datetime.datetime.now().isoformat().replace(":","_").replace(".", "_")


list_of_ports = list(serial.tools.list_ports.comports())
print('All ports', list_of_ports)

if not list_of_ports:
    print('no port is available')
    exit(0x01)

print(f'try to connect to {list_of_ports[0].name}')
serial_port = serial.Serial(port=f'/dev/{list_of_ports[0].name}', baudrate=115200, timeout=.1)

ind = 0
last_cake = datetime.datetime.now()
cake_status = True
cake_norms = np.zeros(10)

if not os.path.isdir(face_path):
    os.makedirs(face_path)
    
cap = cv2.VideoCapture(0)
        
# dump some images
print(f'{timestamp()}: dump 100 frames')
for _ in range(100):
    _, img = cap.read()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
print(f'{timestamp()}: start real capture')
try:
    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # faces = face_recognition.face_locations(img)
        if len(faces) > 0:
            # print(f'{timestamp()}: eyes detected')
            with open(eyes_output_path, 'w') as f:
                f.write(datetime.datetime.now().isoformat())
            if (datetime.datetime.now() - lasteyes).total_seconds() > INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS:
                print(f'{timestamp()}: those are new eyes, save to faces')
                cv2.imwrite(os.path.join(face_path, f'{timestamp()}.png'), img)
                lasteyes = datetime.datetime.now()
        
        cake_algo = list(map(int, requests.get('http://localhost:5000/getalgo').text.split(',')))
        is_it_cake = np.linalg.norm(np.array([255,255,255]) - img[cake_algo[1], cake_algo[0]])
        ind = (ind + 1) % cake_norms.shape[0]
        cake_norms[ind] = is_it_cake

        # last_cake
        if ind % 10 == 0: # check for cake status
            cur_cake_status = np.mean(cake_norms) < cake_algo[3]
            print(f'cur cake status {cur_cake_status}')
            if not cur_cake_status and cake_status:
                print('need to replace cake')
                serial_port.write(b"switch\n")
            cake_status = cur_cake_status

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # for (t, l, b, r) in faces:
        #     cv2.rectangle(img, (l, t), (r, b), (255, 0, 0), 2)
        cv2.drawMarker(img, cake_algo[:2], (255,0,0) if cake_status else (0, 0, 255))
        # cv2.imshow('image', img)
        # cv2.waitKey(0) 
        cv2.imwrite('static/cur.png', img)
finally:
    cap.release()

# %%
