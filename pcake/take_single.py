# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os.path
import os

cap = cv2.VideoCapture(0)
# dump some images
print(f'dump 10 frames')
for _ in range(100):
    _, img = cap.read()

_, img = cap.read()
cv2.imwrite('static/cur.png', img)
cap.release()
print('done')
# %%
