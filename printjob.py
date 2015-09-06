import RPi.GPIO as GPIO
import sys, numpy, os, time, signal

# Pin numbers for paper feed
feedenable = 7
feeddir = 11
feedstep = 13

# Pin numbers for drawing axis
linearenable = 15
lineardir = 12
linearstep = 16
linearleft = GPIO.LOW
linearright = GPIO.HIGH

# Printig defs
linewidth = 2   # in feed-steps
maxaspect = 1.4   # height/width

# Servo defs
servopin = 0
servo = GPIO.PWM(servopin, 50)  # 50Hz



def main():
    GPIO.setmode(GPIO.BOARD)
    # Setup pins
    GPIO.setup(feedenable, GPIO.OUT)
    GPIO.setup(feeddir, GPIO.OUT)
    GPIO.setup(feedstep, GPIO.OUT)

    GPIO.setup(linearenable, GPIO.OUT)
    GPIO.setup(lineardir, GPIO.OUT)
    GPIO.setup(linearstep, GPIO.OUT)

    # Enable Stepper drivers
    GPIO.output(feedenable, GPIO.LOW)
    GPIO.output(linearenable, GPIO.LOW)
    
    # Set Feed direction
    GPIO.output(feeddir, GPIO.LOW)
    print("test")
    """if(len(sys.argv) != 2):
        return 2

    # Open job file
    try:
        job = numpy.load(sys.argv[1])
    except IOError:
        return 2
    
    if(processjob(job)):
        return 1
    else:
        return 0"""
    feed(10)
    linear(3000, linearright)
    return 0

    
def processjob(job):
    xlen = job.shape[1]
    ylen = job.shape[0]
    np.flipud(job)

     

    return 1
   
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

def setservo(angle):
    angle = max(min(180, angle), 0)
    print(angle)

if(__name__ == "__main__"):
    try:
        setservo(50)
        setservo(-30)
        setservo(190)
        main()
    except:
        print(sys.exc_info()[0])
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()
 
