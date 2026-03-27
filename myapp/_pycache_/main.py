import cv2
import time
import os
import threading
from people_detection import detect_people_and_aggression

from video_detection import detect_violence
from ragging_engine import ragging_decision
from send_to_django import send_alert
from record_audio import record_audio
from video_buffer import add_frame, save_buffer

# ================= CONFIG =================
SHOW_CAMERA = True
COOLDOWN_SECONDS = 120
EVIDENCE_DIR = "evidence"
FPS = 20
EVENT_DISPLAY_SECONDS = 3
# =========================================




EVENT_ACTIVE = False
EVENT_END_TIME = 0

os.makedirs(EVIDENCE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Camera not accessible")

last_alert_time = 0
alert_active = False
alert_lock = threading.Lock()

def handle_alert(severity, ts):
    global alert_active
    try:
        video_path = f"{EVIDENCE_DIR}/video_{ts}.mp4"
        audio_path = f"{EVIDENCE_DIR}/audio_{ts}.wav"

        save_buffer(video_path, fps=FPS)
        record_audio(audio_path, duration=5)
        send_alert(video_path, audio_path, severity)

        print("🚨 ALERT SENT:", severity)
    finally:
        with alert_lock:
            alert_active = False

print("✅ Anti-Ragging AI Started (Press Q to quit)")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    add_frame(frame)

    people_count, aggressive_motion = detect_people_and_aggression(frame)

    video_flag = False
    if people_count >= 2 and aggressive_motion:
        video_flag = detect_violence(frame)

    audio_flag = False  # optional later
    severity = ragging_decision(video_flag, audio_flag)
    now = time.time()

    # -------- ALERT TRIGGER --------
    with alert_lock:
        if (
            severity and
            not alert_active and
            now - last_alert_time > COOLDOWN_SECONDS
        ):
            alert_active = True
            last_alert_time = now
            ts = int(now)

            EVENT_ACTIVE = True
            EVENT_END_TIME = now + EVENT_DISPLAY_SECONDS

            threading.Thread(
                target=handle_alert,
                args=(severity, ts),
                daemon=True
            ).start()

    # -------- UI DISPLAY --------
    if SHOW_CAMERA:
        if EVENT_ACTIVE:
            status = "HIGH"
            color = (0, 0, 255)
            if time.time() > EVENT_END_TIME:
                EVENT_ACTIVE = False
        else:
            status = "NORMAL"
            color = (0, 255, 0)

        cv2.putText(frame, f"STATUS: {status}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"People: {people_count}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Anti-Ragging Surveillance", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("🛑 Surveillance stopped safely")
