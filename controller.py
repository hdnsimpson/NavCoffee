#!/usr/bin/env python3

import subprocess
from signal import pause
from gpiozero import Button, LED
from time import sleep, time
import RPi.GPIO as GPIO
import threading

START_BUTTON_PIN = 17
STOP_BUTTON_PIN = 27
REDEEM_BUTTON_PIN = 22
START_LED_PIN = 6
COFFEE_AVAILABLE_LED_PIN = 13

start_button = None
stop_button = None
redeem_button = None


def start():
    print("Starting stream")
    GPIO.output(START_LED_PIN, True)
    subprocess.Popen("/home/pi/Documents/stream.sh")

def stop():
    print("Stopping stream")
    GPIO.output(START_LED_PIN, False)
    subprocess.Popen("/home/pi/Documents/stop_stream.sh")

def redeem():
    print("Redeeming cofee")
    redeem_file = open("/home/pi/Documents/redemptions.txt", "r")
    redemptions = redeem_file.readline()
    redemptions = int(redemptions) + 1
    redeem_file.close()

    redeem_file = open("redemptions.txt", "w")
    redeem_file.write(str(redemptions))
    redeem_file.close()

def coffee_available():
    threading.Timer(5.0, coffee_available).start()

    GPIO.setup(COFFEE_AVAILABLE_LED_PIN, GPIO.OUT)
    redeem_file = open("/home/pi/Documents/redemptions.txt", "r")
    redemptions = int(redeem_file.readline())
    redeem_file.close()

    coffee_file = open("/home/pi/Documents/coffees_donated.txt", "r")
    coffees = int(coffee_file.readline())
    coffee_file.close()
    
    if coffees > redemptions:
        GPIO.output(COFFEE_AVAILABLE_LED_PIN, True)
    else:
        GPIO.output(COFFEE_AVAILABLE_LED_PIN, False)
        
def check_wallet():
    threading.Timer(30.0, check_wallet).start()
    subprocess.Popen("/home/pi/Documents/query_wallet.sh")

def setup_buttons():
    global start_button, stop_button, redeem_button

    print("Initializing hardware ...")

    start_button = Button(START_BUTTON_PIN)
    start_button.when_pressed = start

    stop_button = Button(STOP_BUTTON_PIN)
    stop_button.when_pressed = stop

    redeem_button = Button(REDEEM_BUTTON_PIN)
    redeem_button.when_pressed = redeem

    GPIO.setup(START_LED_PIN, GPIO.OUT)
    GPIO.output(START_LED_PIN, False)

    GPIO.setup(COFFEE_AVAILABLE_LED_PIN, GPIO.OUT)
    GPIO.output(COFFEE_AVAILABLE_LED_PIN, False)

    check_wallet()
    coffee_available()

    print("Ready")

if __name__ == '__main__':
    setup_buttons()
    pause()
