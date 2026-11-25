import cv2

import math
import os

print("پوشه اجرا:", os.getcwd())
print("پوشه video هست؟", os.path.exists("video"))
print("فایل هست؟", os.path.exists("video/traffic.mp4"))
if os.path.exists("video/traffic.mp4"):
    print("اندازه (MB):", os.path.getsize("video/traffic.mp4") / 1e6)

path = "video/traffic.mp4"
cap = cv2.VideoCapture(path)
if not cap.isOpened():
    raise RuntimeError("Could not open video. Run download_video.py first.")

fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps) if fps > 0 else 30

subtractor = cv2.createBackgroundSubtractorMOG2(
    history=200, varThreshold=40, detectShadows=True)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

MIN_AREA = 800      # blobs smaller than this are ignored
MAX_DIST = 60       # max centroid movement between two frames
count = 0
tracks = {}         # id -> (cx, cy)
next_id = 0
line_y = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    if line_y is None:
        line_y = int(h * 0.6)

    # 1) motion detection
    mask = subtractor.apply(frame)
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # 2) find moving objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for c in contours:
        if cv2.contourArea(c) < MIN_AREA:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
        centers.append((x + bw // 2, y + bh // 2))

    # 3) match with previous frame and count line crossings
    new_tracks = {}
    for (cx, cy) in centers:
        best_id, best_d = None, MAX_DIST
        for tid, (px, py) in tracks.items():
            if tid in new_tracks:
                continue
            d = math.hypot(cx - px, cy - py)
            if d < best_d:
                best_id, best_d = tid, d
        if best_id is None:
            best_id = next_id
            next_id += 1
        else:
            py = tracks[best_id][1]
            if (py < line_y <= cy) or (py >= line_y > cy):
                count += 1
        new_tracks[best_id] = (cx, cy)
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
    tracks = new_tracks

    # 4) draw line and counter
    cv2.line(frame, (0, line_y), (w - 1, line_y), (255, 0, 0), 2)
    cv2.putText(frame, f"Count: {count}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    cv2.imshow("Counter", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(delay) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        line_y = max(0, line_y - 10)
    elif key == ord('s'):
        line_y = min(h - 1, line_y + 10)

print("Final count:", count)
cap.release()
cv2.destroyAllWindows()