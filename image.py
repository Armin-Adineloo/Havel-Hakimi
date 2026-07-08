import cv2 as cv
import numpy as np
from ultralytics import YOLO

# مدل فقط یک بار لود می‌شود
model = YOLO("runs/detect/train-3/weights/best.pt")


def nearest_node(point, nodes):
    """
    نزدیک‌ترین نود به یک نقطه را پیدا می‌کند.
    """

    px, py = point

    best = None
    best_dist = float("inf")

    for i, (nx, ny) in enumerate(nodes):

        dist = np.sqrt((px - nx) ** 2 + (py - ny) ** 2)

        if dist < best_dist:
            best_dist = dist
            best = i

    return best


def image(file_path):
    """
    ورودی:
        مسیر عکس

    خروجی:
        Degree Sequence
    """

    # -----------------------------
    # Read Image
    # -----------------------------
    img = cv.imread(file_path)

    if img is None:
        raise ValueError("Image not found!")

    # -----------------------------
    # Detect Nodes (YOLO)
    # -----------------------------
    results = model(img)

    boxes = results[0].boxes

    nodes = []

    for box in boxes.xywh:

        x, y, w, h = box.tolist()

        nodes.append((int(x), int(y)))

    # مرتب شدن نودها برای ثابت ماندن شماره‌ها
    nodes.sort()

    # -----------------------------
    # Remove Nodes
    # -----------------------------
    clean = img.copy()

    for x, y in nodes:

        cv.circle(
            clean,
            (x, y),
            30,
            (255, 255, 255),
            -1
        )

    # -----------------------------
    # Detect Edges
    # -----------------------------
    gray = cv.cvtColor(clean, cv.COLOR_BGR2GRAY)

    blur = cv.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv.Canny(
        blur,
        50,
        150
    )

    lines = cv.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=60,
        minLineLength=40,
        maxLineGap=40
    )

    # -----------------------------
    # Build Edge List
    # -----------------------------
    edge_list = set()

    if lines is not None:

        for line in lines:

            x1, y1, x2, y2 = line[0]

            node1 = nearest_node((x1, y1), nodes)
            node2 = nearest_node((x2, y2), nodes)

            if node1 is None or node2 is None:
                continue

            if node1 == node2:
                continue

            edge = tuple(sorted((node1, node2)))

            edge_list.add(edge)

    edge_list = sorted(edge_list)

    # -----------------------------
    # Degree Sequence
    # -----------------------------
    degrees = [0] * len(nodes)

    for u, v in edge_list:

        degrees[u] += 1
        degrees[v] += 1

    return degrees
