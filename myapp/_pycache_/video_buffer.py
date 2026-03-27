from collections import deque
import threading
import cv2

BUFFER_SIZE = 60  # ~3 seconds at 20 FPS
_frame_buffer = deque(maxlen=BUFFER_SIZE)
_buffer_lock = threading.Lock()

def add_frame(frame):
    with _buffer_lock:
        _frame_buffer.append(frame.copy())

def get_buffer_copy():
    with _buffer_lock:
        return list(_frame_buffer)

def save_buffer(filename, fps=20):
    frames = get_buffer_copy()
    if not frames:
        return

    h, w, _ = frames[0].shape
    out = cv2.VideoWriter(
        filename.replace(".avi", ".mp4"),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h)
    )

    for f in frames:
        out.write(f)

    out.release()
