#!/bin/python

import time, sys, signal
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

def exitgracefully():
	GPIO.cleanup()

def siginthandler(signal, frame):
	exitgracefully()

signal.signal(signal.SIGINT, siginthandler)


GPIO.setup(7, GPIO.OUT) 	# Driver Enable output
GPIO.output(7, GPIO.LOW)	# Enable stepper drivers

GPIO.setup(11, GPIO.OUT)	# DIR 1
GPIO.output(11, GPIO.HIGH)	# *unicode shrug*

GPIO.setup(13, GPIO.OUT)
GPIO.output(11,GPIO.HIGH)
for i in range(3000):
	GPIO.output(13, GPIO.HIGH)
	time.sleep(0.001)

	GPIO.output(13, GPIO.LOW)
	time.sleep(0.001)

GPIO.output(11,GPIO.LOW)
for i in range(3000):
	GPIO.output(13, GPIO.HIGH)
	time.sleep(0.001)

	GPIO.output(13, GPIO.LOW)
	time.sleep(0.001)
	
exitgracefully()
