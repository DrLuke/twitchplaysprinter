import RPi.GPIO as GPIO
import sys, numpy, os, time, signal

# Pin numbers for paper feed
feedenable = 7
feeddir = 11
feedstep = 13

# Defs for drawing axis
linearenable = 15
lineardir = 12
linearstep = 16
linearleft = GPIO.LOW
linearright = GPIO.HIGH
stepintegrator = 0

# Servo defs
servopin = 26
servodown = 28.0
servoup = 15.0



   
def feed(steps):
    for i in range(steps):
        GPIO.output(feedstep, GPIO.HIGH)
        time.sleep(0.025)
        GPIO.output(feedstep, GPIO.LOW)
        time.sleep(0.025)

def linear(steps, direction):
    GPIO.output(lineardir, direction)
    for i in range(steps):
        GPIO.output(linearstep, GPIO.HIGH)
        time.sleep(0.0004)
        GPIO.output(linearstep, GPIO.LOW)
        time.sleep(0.0004)

def main():
    global stepintegrator
    GPIO.setmode(GPIO.BOARD)
    # Setup pins
    GPIO.setup(feedenable, GPIO.OUT)
    GPIO.setup(feeddir, GPIO.OUT)
    GPIO.setup(feedstep, GPIO.OUT)

    GPIO.setup(linearenable, GPIO.OUT)
    GPIO.setup(lineardir, GPIO.OUT)
    GPIO.setup(linearstep, GPIO.OUT)

    GPIO.setup(servopin, GPIO.OUT)

    # Enable Stepper drivers
    GPIO.output(feedenable, GPIO.LOW)
    GPIO.output(linearenable, GPIO.LOW)
    
    # Set Feed direction
    GPIO.output(feeddir, GPIO.HIGH)

    #feed(10)
    linear(4000, linearleft)

if __name__ == "__main__":
    main()
    GPIO.cleanup()
