import cv2
import numpy as np
import time
from collections import deque
import tensorflow as tf
import os

# ---- LOAD MODEL ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "violence_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# ---- SIMPLE STATE ----
CONF_BUFFER = deque(maxlen=3)   # only last 3 frames
THRESHOLD = 0.6
COOLDOWN = 5                    # seconds
last_sent_time = 0

def detect_violence(frame):
    global last_sent_time

    # preprocess
    frame = cv2.resize(frame, (224, 224))
    frame = frame.astype("float32") / 255.0
    frame = np.expand_dims(frame, axis=0)

    confidence = float(model.predict(frame, verbose=0)[0][0])
    CONF_BUFFER.append(confidence)

    now = time.time()

    print(f"[ML] Conf: {confidence:.2f} | Buffer: {[round(c,2) for c in CONF_BUFFER]}")

    # cooldown check (ONLY spam protection)
    if now - last_sent_time < COOLDOWN:
        return False

    # SEND RULE: 2 out of last 3 frames above threshold
    strong_frames = sum(1 for c in CONF_BUFFER if c >= THRESHOLD)

    if strong_frames >= 2:
        last_sent_time = now
        print("🚨 VIOLENCE TRIGGERED – SENDING ALERT")
        return True

    return False
