import cv2
import time
import subprocess

def record_video2(file, delay):
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # 0 represents the default camera (first available camera)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs as well, such as MJPG
    out = cv2.VideoWriter(file, fourcc, 20.0, (640, 480))  # Adjust resolution and fps as needed

    # Start capturing and recording
    start_time = time.time()
    while camera.isOpened():
        ret, frame = camera.read()
        if ret:
            # Write the frame to the video file
            out.write(frame)
            
            # Stop recording after 20 seconds
            if time.time() - start_time > delay:
                break
        else:
            break

    # Release everything when finished
    camera.release()
    out.release()
    cv2.destroyAllWindows()

