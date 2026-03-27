import requests

DJANGO_URL = "http://127.0.0.1:8000/myapp/ragging-alert/"

def send_alert(video_file, audio_file, severity):
    try:
        with open(video_file, "rb") as v, open(audio_file, "rb") as a:
            response = requests.post(
                DJANGO_URL,
                files={
                    "video": v,
                    "audio": a
                },
                data={"severity": severity},
                timeout=10
            )

        print("📡 Django response:", response.status_code)

    except requests.exceptions.ConnectionError:
        print("❌ Django server not reachable. Is runserver running?")
    except Exception as e:
        print("❌ Error sending alert:", e)
