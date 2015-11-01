#!/usr/bin/python3

import printercontrol, numpy, time

# Printig defs
linewidth = 2  # in feed-steps
maxaspect = 1.4  # height/width
maxpixelwidth = 500  # in linear-steps
paperwidth = 20000  # in linear-steps

def main():
    with open("printjob.log", "a") as logfile:
        logfile.write("\r\n\r\n******************\r\nStarting program\r\n")
        p = printercontrol.printercontrols()

        while(1):
            newJobfile = getNewJob()
            try:
                job = numpy.load(newJobfile)
            except IOError:
                logfile.write("Error opening file: " + newJobfile + "\r\n")

            print(job)
            if (processjob(job, p)):
                return 1
            else:
                return 0

def getNewJob():
    return "newjob" #FIXME: Actually get a new job

def processjob(job, p):

    xlen = job.shape[1]
    ylen = job.shape[0]
    print("xlen: " + str(xlen))
    pixelwidth = min(maxpixelwidth, paperwidth / xlen)
    pixelheight = max(1, int(pixelwidth / 100))
    print("Pixelwidth: " + str(pixelwidth))
    # numpy.flipud(job)

    if (ylen / xlen > maxaspect):
        print("ylen/xlen: " + str(ylen / xlen))
        return 1

    for row in job:
        for rep in range(pixelheight):
            if (printrow(row, pixelwidth, p)):
                return 1

    for i in range(40):
        p.moveFeed(2)
        time.sleep(0.05)

    return 0


def printrow(row, pixelsize, p):
    global stepintegrator

    # # Move to starting position
    # startpos = paperwidth / 2 - (len(row) * pixelsize) / 2
    # if (stepintegrator > startpos):
    #     linear(stepintegrator - startpos, linearleft)
    #     stepintegrator -= stepintegrator - startpos
    # elif (stepintegrator < startpos):
    #     linear(startpos - stepintegrator, linearright)
    #     stepintegrator += startpos - stepintegrator
    # else:
    #     print("Already at startposition!")
    #
    #
    #
    # for pixel in row:
    #     if (int(pixel) == 1):
    #         servo.ChangeDutyCycle(servodown)
    #     else:
    #         servo.ChangeDutyCycle(servoup)
    #     linear(pixelsize, linearright)
    #     stepintegrator += pixelsize
    # # Safely reset servo and give it some time
    # servo.ChangeDutyCycle(servoup)
    # time.sleep(0.6)
    # servo.stop()
    # feed(linewidth)

    startpixel = 0
    for pixel in line:
        if int(pixel) == 0:
            startpixel += 1
        else:
            break

    startposition = startpixel * pixelsize

    if p.linearStepIntegrator < startposition:
        p.moveLinear(p.linearRight, startposition-p.linearStepIntegrator)
    elif p.linearStepIntegrator > startposition:
        p.moveLinear(p.linearLeft, p.linearStepIntegrator-startposition)

if (__name__ == "__main__"):
    main()
