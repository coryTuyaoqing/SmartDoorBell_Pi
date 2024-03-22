import RPi.GPIO as GPIO
import time
from gpiozero import Button

magnet = Button(20)
button = Button(16)

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO 6 as output
transistor_pin = 6
GPIO.setup(transistor_pin, GPIO.OUT)

def lock_door():
    """
    Function to lock the door by turning on the transistor.
    """
    GPIO.output(transistor_pin, GPIO.HIGH)
    print("Door locked")

def unlock_door():
    """
    Function to unlock the door by turning off the transistor.
    """
    GPIO.output(transistor_pin, GPIO.LOW)
    print("Door unlocked")

def Door_Status():
    """
    Function to check the status of the door.
    """
    if magnet.value == 1:
        print("door closed")
        return False
    elif magnet.value == 0:
        print("door open")
        return True
