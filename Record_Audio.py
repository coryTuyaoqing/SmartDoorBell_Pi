from threading import Thread
from gpiozero import MCP3008
import time
import wave
import numpy as np


def record_audio(output_file, duration):
    pot = MCP3008(channel=0)
    voltage_list = []
    fs = 5000
    T = 1 / fs
    t_start = time.monotonic()
    t_last = t_start
    t_end = t_start + duration

    while time.monotonic() < t_end:
        if time.monotonic() - t_last > T:
            voltage_list.append(pot.value * 3.3 - 3.3/2)
            t_last = t_last + T

    print("Recording complete.")

    output_file = "audio.wav"  # Name of the output file
    n_channels = 1  # Number of audio channels (1 for mono, 2 for stereo)
    sample_width = 2  # Sample width in bytes (2 for 16-bit audio)
    frame_rate = fs # Frame rate (samples per second)
    audio_data = np.array(voltage_list)

    # Create a wave file object
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        # Convert the audio data to bytes and write to the file
        audio_bytes = np.int16(audio_data * 32767)  # Convert float audio to 16-bit
        wav_file.writeframes(audio_bytes.tobytes())
        print(f"Audio saved as '{output_file}'.")

    
