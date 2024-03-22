import picamera


def record_video(duration=20, filename="video.h264"):
    try:
        with picamera.PiCamera() as camera:
            camera.start_recording(filename)
            camera.wait_recording(duration)
            camera.stop_recording()
        print(f"Video recorded and saved as {filename}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    record_video()
