import time, printercontrol

def main():
    p = printercontrol.printercontrols()
    p.homed = True

    p.moveLinear(p.linearRight, 1000)


if __name__ == "__main__":
    main()
