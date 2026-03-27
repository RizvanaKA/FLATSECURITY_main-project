import cv2
import os

from django.conf import settings

from myapp.models import RaggingEvidence, User_table, RaggingInvolvedStudent


def recognize_students_from_video(evidence_id):
    print("🔍 DeepFace recognition started")
    print("🧠 Face recognition service loaded")

    try:
        evidence = RaggingEvidence.objects.get(id=evidence_id)
    except:
        print("❌ Evidence not found")
        return

    video_path = os.path.join(settings.MEDIA_ROOT, evidence.video.name)
    print("🎥 Video:", video_path)

    students = User_table.objects.exclude(photo="")
    print(f"👥 Students: {students.count()}")

    cap = cv2.VideoCapture(video_path)
    frame_no = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_no += 1
        if frame_no % 15 != 0:
            continue

        for student in students:
            student_img = os.path.join(settings.MEDIA_ROOT, student.photo.name)

            try:
                result = DeepFace.verify(
                    img1_path=student_img,
                    img2_path=frame,
                    model_name="Facenet",
                    detector_backend="mtcnn",
                    enforce_detection=False
                )

                if result["verified"]:
                    confidence = 1 - result["distance"]

                    RaggingInvolvedStudent.objects.get_or_create(
                        STUDENT=student,
                        EVIDENCE=evidence,
                        defaults={"confidence": confidence}
                    )

                    print(f"✅ MATCH: {student.name} ({confidence:.2f})")

            except Exception as e:
                print("⚠️ Face check skipped:", e)

    cap.release()
    print("🏁 Recognition finished")
