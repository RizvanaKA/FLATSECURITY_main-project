import cv2
import requests
import time

URL = "http://127.0.0.1:8000/myapp/check_stranger_api/"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
last_check_time = 0

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If a face is found, check every 3 seconds
    if len(faces) > 0 and (time.time() - last_check_time > 3):
        last_check_time = time.time()

        # Encode and send to Django
        _, img_encoded = cv2.imencode('.jpg', frame)
        files = {'image': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}

        try:
            response = requests.post(URL, files=files)
            print("Server Response:", response.json())
        except Exception as e:
            print("Connection Error:", e)

    # Draw box for visual feedback
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Stranger Detection Mode", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()