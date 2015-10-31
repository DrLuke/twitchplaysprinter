import time, printercontrol, sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--linear", help="Amount to move on linear axis", default=0, type=int)
    parser.add_argument("-f", "--feed", help="Amount to move on feed axis", default=0, type=int)
    parser.add_argument("-s", "--servo", help="Position servo in 'up' or 'down' position", default="", type=str)


    args = parser.parse_args()

    p = printercontrol.printercontrols()
    p.homed = True
    p.ignoreIntegrator = True

    if args.linear > 0:
        p.moveLinear(p.linearRight, args.linear)
    elif args.linear < 0:
        p.moveLinear(p.linearLeft, -args.linear)

    if args.feed > 0:
        p.moveFeed(args.feed)

    if args.servo == "up":
        p.positionServo(p.servoUp)
        time.sleep(1)
    elif args.servo == "down":
        p.positionServo(p.servoDown)
        time.sleep(1)

if __name__ == "__main__":
    main()


