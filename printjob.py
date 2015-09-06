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

# Printig defs
linewidth = 2   # in feed-steps
maxaspect = 1.4   # height/width
maxpixelwidth = 500	# in linear-steps
paperwidth = 7000	# in linear-steps

# Servo defs
servopin = 26
servodown = 28.0
servoup = 15.0


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
    
    # Start servo PWM
   
    if(len(sys.argv) != 2):
        return 2
    
    # Open job file
    job = numpy.load(sys.argv[1])
    try:
        job = numpy.load(sys.argv[1])
    except IOError:
	print("Couldn't open file")
        return 2
    
    print(job) 
    if(processjob(job)):
        return 1
    else:
        return 0
    #servo.ChangeDutyCycle(15.0)
    #time.sleep(2)
    #feed(10)
    #servo.ChangeDutyCycle(30.0)
    #linear(3000, linearleft)
    #feed(10)
    #linear(3000, linearleft)
    #servo.ChangeDutyCycle(15.0)
    #time.sleep(2)
    return 0

    
def processjob(job):
    global stepintegrator

    xlen = job.shape[1]
    ylen = job.shape[0]
    print("xlen: " + str(xlen))
    pixelwidth = min(maxpixelwidth, paperwidth/xlen)
    pixelheight = min(1,int(pixelwidth/100))
    print("Pixelwidth: " + str(pixelwidth))
    numpy.flipud(job)

    if(ylen/xlen > maxaspect):
	print("ylen/xlen: " + str(ylen/xlen))
	return 1

    for row in job:
	for rep in range(pixelheight):
	    if(printrow(row,pixelwidth)):
	        return 1

    if(stepintegrator > 0):
	linear(stepintegrator, linearleft)

    feed(20)

    return 0

def printrow(row, pixelsize):
    global stepintegrator
    servo = GPIO.PWM(servopin, 100.0)  # 50Hz
    servo.start(servoup)
  
    # Move to starting position
    startpos = paperwidth/2 - (len(row)*pixelsize)/2
    if(stepintegrator > startpos):
        linear(stepintegrator-startpos, linearleft)
        stepintegrator -= stepintegrator-startpos
    elif(stepintegrator < startpos):
        linear(startpos-stepintegrator, linearright)
        stepintegrator += startpos-stepintegrator
    else:
        print("Already at startposition!")
    
    for pixel in row:
        if(int(pixel) == 1):
    	    servo.ChangeDutyCycle(servodown)
	else:
	    servo.ChangeDutyCycle(servoup)
	linear(pixelsize, linearright)
	stepintegrator += pixelsize
    servo.stop()
    feed(linewidth)
   
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

if(__name__ == "__main__"):
    main()
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()
 
