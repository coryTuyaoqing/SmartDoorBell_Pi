# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(16,GPIO.IN)

# def input_change(channel):
#     print()

# GPIO.add_event_callback(16, GPIO.RISING, callback=input_change)

# # while True:
#     print(GPIO.input(16))

from gpiozero import Button
from threading import Thread

button = Button(16)

def detect_input_change():
    def input_change():
        print(button.value)
    button.when_deactivated = input_change
    while True: pass

t = Thread(target=detect_input_change)
t.start()
