import pygame
import ffmpeg

def play_audio(file_path, file_name):
    input_file = file_path + file_name
    output_file = file_path + 'output.wav'

    # Run ffmpeg command to convert 3GP to WAV
    ffmpeg.input(input_file).output(output_file).run()

    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
