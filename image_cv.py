import cv2 as cv
import numpy as np

def image(file):
    img = cv.imread(file)
    gray_img = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray_img, (9, 9), 2)
    cv.imshow('graph',blur)
    cv.waitKey(0)
    cv.destroyAllWindows()

    #nodes
    circles = cv.HoughCircles(
        blur,
        cv.HOUGH_GRADIENT,
        dp=1.2,
        minDist=100,
        param1=50,
        param2=10,
        minRadius=40,
        maxRadius=100
    )

    if circles is None:
        print("No circles detected")

    circles = np.uint16(np.around(circles[0]))

    nodes = []
    for i, c in enumerate(circles):
        x, y, r = c
        nodes.append((i, (x, y)))

    #edges
    edges_img = cv.Canny(blur, 50, 150)

    lines = cv.HoughLinesP(
        edges_img,
        1,
        np.pi / 180,
        threshold=80,
        minLineLength=50,
        maxLineGap=10
    )

    if lines is None:
        print("No lines detected")
        return []

    #edge list
    def nearest_node(point):
        px, py = point
        best = None
        best_dist = float("inf")

        for node_id, (nx, ny) in nodes:
            dist = np.sqrt((px - nx)**2 + (py - ny)**2)
            if dist < best_dist:
                best_dist = dist
                best = node_id

        return best

    edge_list = set()

    for line in lines:
        x1, y1, x2, y2 = line[0]

        n1 = nearest_node((x1, y1))
        n2 = nearest_node((x2, y2))

        if n1 is not None and n2 is not None and n1 != n2:
            edge_list.add(tuple(sorted((n1, n2))))

    edge_list = list(edge_list)

    print("Nodes:", nodes)
    print("Edges:", edge_list)

    return edge_list
