import sys, numpy, os, time

def main():
    if(len(sys.argv) != 2):
        return 2
    try:
        job = numpy.load(sys.argv[1])
    except IOError:
        return 2
    
    
    time.sleep(2)



    return 0


if(__name__ == "__main__"):
    main()
