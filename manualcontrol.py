import time, printercontrol, sys

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def main():
    p = printercontrol.printercontrols()
    p.homed = True

    while(1):
        getch = _GetchUnix()
        char = getch()

        print(char)
        if char is "\x03":
            print("Exiting...")
            sys.exit(0)
        elif char is "d":
            print("Right 100")
            p.moveLinear(p.linearRight, 100)
        elif char is "D":
            print("Right 1000")
            p.moveLinear(p.linearRight, 1000)
        elif char is "a":
            print("Left 100")
            p.moveLinear(p.linearLeft, 100)
        elif char is "A":
            print("Left 1000")
            p.moveLinear(p.linearLeft, 1000)




if __name__ == "__main__":
    main()

