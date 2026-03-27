import numpy as np

def detect_distress(audio_chunk):
    volume = np.linalg.norm(audio_chunk)
    return volume > 6000
