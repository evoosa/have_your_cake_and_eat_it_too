# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os.path
import os
import face_recognition
import requests
import cake

# %%
INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS = 100
eyes_output_path = 'static/lasteyes.txt'
cake_output_path = 'static/cake.txt'
face_path = 'static/faces'
lasteyes = datetime.datetime.now() - datetime.timedelta(days=1)
timestamp = lambda: datetime.datetime.now().isoformat().replace(":","_").replace(".", "_")


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

print(f'{timestamp()}: start real capture')
try:
    while True:
        _, img = cap.read()
        
        faces = face_recognition.face_locations(img)
        if len(faces) > 0:
            # print(f'{timestamp()}: eyes detected')
            with open(eyes_output_path, 'w') as f:
                f.write(datetime.datetime.now().isoformat())
            if (datetime.datetime.now() - lasteyes).total_seconds() > INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS:
                print(f'{timestamp()}: those are new eyes, save to faces')
                cv2.imwrite(os.path.join(face_path, f'{timestamp()}.png'), img)
                lasteyes = datetime.datetime.now()
        
        cakepixel = list(map(int, requests.get('http://localhost:5000/getcakepixel').text.split(',')))
        is_it_cake = np.linalg.norm(np.array([255,255,255]) - img[cakepixel[1], cakepixel[0]])
        ind = (ind + 1) % cake_norms.shape[0]
        cake_norms[ind] = is_it_cake

        # last_cake
        if ind % 10 == 0: # check for cake status
            cur_cake_status = np.mean(cake_norms) < 50
            print(f'cur cake status {cur_cake_status}')
            if not cur_cake_status and cake_status:
                print('need to replace cake')
            cake_status = cur_cake_status

        for (t, l, b, r) in faces:
            cv2.rectangle(img, (l, t), (r, b), (255, 0, 0), 2)
        cv2.drawMarker(img, cakepixel, (255,0,0) if cake_status else (0, 0, 255))
        # cv2.imshow('image', img)
        # cv2.waitKey(0) 
        cv2.imwrite('static/cur.png', img)
finally:
    cap.release()

# %%
