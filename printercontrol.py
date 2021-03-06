import time
import RPi.GPIO as GPIO

__author__ = 'drluke'



class printercontrols:
    def __init__(self):
        self.homed = False

        # Linear drawing axis
        self.linearEnable = 15
        self.linearDir = 12
        self.linearStep = 16
        self.linearLeft = GPIO.LOW
        self.linearRight = GPIO.HIGH
        self.linearStepIntegrator = 0
        self.ignoreIntegrator = False
        self.paperWidth = 20000

        # Paper feed
        self.feedEnable = 7
        self.feedDir = 11
        self.feedStep = 13

        # Pen servo
        self.servoPin = 26
        self.servoDown = 28.0
        self.servoUp = 15.0

        # Set up GPIO
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.linearEnable, GPIO.OUT)
        GPIO.setup(self.linearDir, GPIO.OUT)
        GPIO.setup(self.linearStep, GPIO.OUT)

        GPIO.setup(self.feedEnable, GPIO.OUT)
        GPIO.setup(self.feedDir, GPIO.OUT)
        GPIO.setup(self.feedStep, GPIO.OUT)

        GPIO.setup(self.servoPin, GPIO.OUT)
        self.servo = GPIO.PWM(self.servoPin, 100.0) # 50Hz

        GPIO.output(self.feedEnable, GPIO.LOW)
        GPIO.output(self.linearEnable, GPIO.LOW)

        GPIO.output(self.feedDir, GPIO.HIGH)

    def home(self):
        self.homed = True # FIXME: Add code to actually home in the linear axis!

    def moveLinear(self, dir, steps):
        if self.homed:
            GPIO.output(self.linearDir, dir)
            for i in range(steps):
                if dir == self.linearLeft:
                    if self.linearStepIntegrator > 0 or self.ignoreIntegrator:
                        self.linearStepIntegrator -= 1
                        GPIO.output(self.linearStep, GPIO.HIGH)
                        time.sleep(0.0004)
                        GPIO.output(self.linearStep, GPIO.LOW)
                        time.sleep(0.0004)
                    else:
                        print("Reached linear negative limit!")
                        break
                elif dir == self.linearRight:
                    if self.linearStepIntegrator < self.paperWidth or self.ignoreIntegrator:
                        self.linearStepIntegrator += 1
                        GPIO.output(self.linearStep, GPIO.HIGH)
                        time.sleep(0.0004)
                        GPIO.output(self.linearStep, GPIO.LOW)
                        time.sleep(0.0004)
                    else:
                        print("Reached linear positive limit!")
                        break

        else:
            print("Not yet homed")

    def moveFeed(self, steps):
        if self.homed:
            for i in range(steps):
                GPIO.output(self.feedStep, GPIO.HIGH)
                time.sleep(0.05)
                GPIO.output(self.feedStep, GPIO.LOW)
                time.sleep(0.05)
        else:
            print("Not yet homed")

    def positionServo(self, position, stopservo=False):
        if stopservo:
            self.servo.stop()
        else:
            self.servo.start(position)
            self.servo.ChangeDutyCycle(position)


    def __del__(self):
        GPIO.cleanup()