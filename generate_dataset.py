import os
import random
import cv2 as cv
import numpy as np


os.makedirs("dataset/images/train", exist_ok=True)
os.makedirs("dataset/images/val", exist_ok=True)
os.makedirs("dataset/labels/train", exist_ok=True)
os.makedirs("dataset/labels/val", exist_ok=True)


def valid_position(x, y, nodes):
    for nx, ny in nodes:
        distance = np.sqrt((x - nx) ** 2 + (y - ny) ** 2)
        if distance < 80:
            return False
    return True


def generate_graph(index):
    NUM_NODES = 6
    EXTRA_EDGES = 3
    WIDTH = 640
    HEIGHT = 640

    img = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

    nodes = []
    while len(nodes) < NUM_NODES:
        x = random.randint(80,560)
        y = random.randint(80,560)
        if valid_position(x, y, nodes):
            nodes.append((x,y))

    edges = []
    for i in range(1, len(nodes)):
        parent = random.randint(0, i - 1)
        edges.append((parent, i))
    while EXTRA_EDGES > 0:
        a = random.randint(0, len(nodes) - 1)
        b = random.randint(0, len(nodes) - 1)
        if a == b:
            continue
        edge = tuple(sorted((a, b)))
        if edge not in edges:
            edges.append(edge)
            EXTRA_EDGES -= 1

    for a,b in edges:
        x1,y1 = nodes[a]
        x2,y2 = nodes[b]
        cv.line(
            img,
            (x1,y1),
            (x2,y2),
            (0,0,0),
            2
        )

    for x, y in nodes:
        cv.circle(
            img,
            (x, y),
            25,
            (0,0,0),
            2
        )

    label_lines = []
    for x, y in nodes:
        x_center = x / WIDTH
        y_center = y / HEIGHT
        box_width = 50 / WIDTH
        box_height = 50 / HEIGHT
        line = f"0 {x_center} {y_center} {box_width} {box_height}"
        label_lines.append(line)

    if index < 1600:
        image_path = f"dataset/images/train/graph_{index}.png"
        label_path = f"dataset/labels/train/graph_{index}.txt"
    else:
        image_path = f"dataset/images/val/graph_{index}.png"
        label_path = f"dataset/labels/val/graph_{index}.txt"

    with open(label_path , "w") as f:
        f.write("\n".join(label_lines))

    cv.imwrite(image_path, img)


for i in range(2000):
    generate_graph(i)
print("Dataset Created Successfully!")
