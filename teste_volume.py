import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
BLOCK_DURATION = 0.05
block_size = int(SAMPLE_RATE * BLOCK_DURATION)

print("Fale ou bata palma perto do microfone... (Ctrl+C pra parar)")
with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=block_size) as stream:
    while True:
        indata, _ = stream.read(block_size)
        volume = float(np.sqrt(np.mean(indata**2)))
        print(f"Volume: {volume:.4f}")