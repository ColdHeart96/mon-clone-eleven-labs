from kokoro import KPipeline
import soundfile as sf
import torch
import numpy as np

print("Device:", "GPU" if torch.cuda.is_available() else "CPU")

pipeline = KPipeline(lang_code='a')

text = """
Hello, this is a test of Kokoro version zero point nineteen.
It is a lightweight but very high quality text to speech model.
The voice sounds natural, with good intonation and clarity.
"""

voice = 'af_heart'

generator = pipeline(text, voice=voice)

all_audio = []

for i, (gs, ps, audio) in enumerate(generator):
    all_audio.append(audio)

final_audio = np.concatenate(all_audio)

sf.write("output_full.wav", final_audio, 24000)
print("Sauvegardé : output_full.wav")
