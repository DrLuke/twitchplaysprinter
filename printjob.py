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
        p.home()

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
    return "00_testfile.npy" #FIXME: Actually get a new job

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

    for i in range(5):
        p.moveFeed(2)
        time.sleep(0.05)

    return 0


def printrow(row, pixelsize, p):
    startpixel = 0
    for pixel in row:
        if int(pixel) == 0:
            startpixel += 1
        else:
            break

    startposition = startpixel * pixelsize

    if p.linearStepIntegrator < startposition:
        p.moveLinear(p.linearRight, startposition-p.linearStepIntegrator)
    elif p.linearStepIntegrator > startposition:
        p.moveLinear(p.linearLeft, p.linearStepIntegrator-startposition)

    for i in range(startpixel, len(row)):
        if int(row[i]) == 1:
            p.positionServo(p.servoDown)
        else:
            p.positionServo(p.servoUp)
        p.moveLinear(p.linearRight, pixelsize)
        if all([int(a) == 0 for a in row[i:]]):
            break

    p.positionServo(p.servoUp)
    time.sleep(0.5)

    p.moveFeed(1)

if (__name__ == "__main__"):
    main()
