from gpiozero import Button
import numpy as np
from Record_Audio import record_audio
from DoorLocking import *
from flask import Flask, render_template, send_file, request
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
import ffmpeg
from display_audio import * 


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/upload/"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 #1G
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

@app.route('/photo')
def download_photo():
    path = "photo.png"
    return send_file(path, as_attachment=True)

@app.route('/download_audio')
def download_audio():
    #record_audio("audio.wav", 20)
    path = "audio.wav"
    return send_file(path, as_attachment=True)

@app.route('/download_video')
def download_video():
    path = "video.mp4"
    return send_file(path, as_attachment=True)
    

@app.route('/unlock')
def lock():
    if(Door_Status()):
        return "can't close the door."
    else:
        unlock_door()

@app.route('/doorstatus')
def get_door_status():
    if(Door_Status()):
        return "open"
    else:
        return "close"

@app.route('/upload_audio', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        # Here you should save the file
        file.save('static/upload/' + filename)
############################################################ todo: test this code
        play_audio('static/upload/' + filename)
############################################################        
        return 'upload successfully!'

    return 'No file uploaded'

@socketio.on('connect')
def handle_connect():
    print('Client connected')

# @socketio.on('monitor_request')
# def handle_monitor_request(message):
#     print('receive monitor request: ', message)

#     # process = (
#     #     ffmpeg
#     #     .input('video.mp4')  # Adjust this path based on your camera device
#     #     .output('pipe:', format='rawvideo', pix_fmt='rgb24')
#     #     .run_async(pipe_stdout=True)
#     # )

#     # while True:
#     #     frame = process.stdout.read(480, 640, 3)  # Adjust frame size as needed
        
#     #     # Convert the raw frame data to a numpy array
#     #     np_frame = np.frombuffer(frame, np.uint8).reshape(480, 640, 3)
        
#     #     # Encode the frame to JPEG format
#     #     jpeg_frame, _ = (
#     #         ffmpeg
#     #         .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='640x480')
#     #         .output('pipe:', format='mjpeg')
#     #         .run(input=np_frame.tobytes(), capture_stdout=True)
#     #     )

#     #     socketio.emit('video_chunk', jpeg_frame)

#     # Open and read the video file
#     with open('video.mp4', 'rb') as video_file:
#         while True:
#             chunk = video_file.read(512)  # Read a chunk of the video file
#             if not chunk:
#                 break
#             socketio.emit('video_chunk', chunk)  # Emit the chunk with the event name 'video_chunk'


def detect_input_change():
    def input_change():
        print(button.value)
        print("Some one is at the door!")
        socketio.send("Some one is at the door!")
    button.when_activated = input_change
    while True: pass

def detect_door_open():
    def door_open():
        print("door is opened")
        socketio.send("The door is opened")
        
    def door_close():
        print("door is closed")
        lock_door()
        socketio.send("The door is closed")

    magnet.when_activated = door_open
    magnet.when_deactivated = door_close
    while True: pass

if __name__ == '__main__':
    socketio.start_background_task(detect_input_change)
    socketio.start_background_task(detect_door_open)
    socketio.run(host='0.0.0.0', port='80', app=app)



