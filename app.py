from gpiozero import Button
from Record_Audio import record_audio
from DoorLocking import *
from flask import Flask, render_template, send_file, request
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO


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
    record_audio("audio.wav", 20)
    path = "audio.wav"
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
        return 'upload successfully!'

    return 'No file uploaded'

@socketio.on('connect')
def handle_connect():
    print('Client connected')



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
    # t = Thread(target=detect_input_change)
    # t.start()
    # print("thread started.")
    socketio.start_background_task(detect_input_change)
    socketio.start_background_task(detect_door_open)
    socketio.run(host='0.0.0.0', port='80', app=app)



