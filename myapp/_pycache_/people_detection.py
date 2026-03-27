import cv2
import numpy as np

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

prev_centers = []
prev_speeds = []

def detect_people_and_aggression(frame):
    global prev_centers, prev_speeds

    boxes, _ = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )

    centers = []
    for (x, y, w, h) in boxes:
        centers.append((x + w // 2, y + h // 2))

    speeds = []
    aggressive = False

    if len(prev_centers) >= 2 and len(centers) >= 2:
        min_p = min(len(prev_centers), len(centers))

        for i in range(min_p):
            dx = centers[i][0] - prev_centers[i][0]
            dy = centers[i][1] - prev_centers[i][1]
            speed = np.sqrt(dx*dx + dy*dy)
            speeds.append(speed)

        # ---- ASYMMETRY CHECK ----
        if len(speeds) >= 2:
            max_speed = max(speeds)
            min_speed = min(speeds)

            # Dominance condition:
            # one person very fast, other relatively slow
            if max_speed > 30 and min_speed < 10:
                aggressive = True

    prev_centers = centers
    prev_speeds = speeds

    return len(centers), aggressive
