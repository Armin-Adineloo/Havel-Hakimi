import os
import random
import cv2 as cv
import numpy as np

def valid_position(x, y, nodes):
    for nx, ny in nodes:
        distance = np.sqrt((x-nx)**2 + (y-ny)**2)
        if distance < 80:
            return False
    return True

os.makedirs("dataset/images/train", exist_ok=True)
os.makedirs("dataset/images/val", exist_ok=True)
os.makedirs("dataset/labels/train", exist_ok=True)
os.makedirs("dataset/labels/val", exist_ok=True)

WIDTH = 640
HEIGHT = 640
img = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

nodes = []
while len(nodes) < 6:
    x = random.randint(80,560)
    y = random.randint(80,560)
    if valid_position(x, y, nodes):
        nodes.append((x,y))

for x, y in nodes:
    cv.circle(
        img,
        (x, y),
        25,
        (0,0,0),
        2
    )
cv.imshow("Graph", img)
cv.waitKey(0)
cv.destroyAllWindows()
