from irc import twitchchat
from bot import bot
from printer import printer
import subprocess
import time

def main():
    irc = twitchchat("drluke4", "oauth:vb6vffy4rqtvon9izfi928g3yoytd1", "#drluke4")
    uguu = bot(irc)
    pri = printer(uguu)

    irc.addcommand(uguu.drawmatrixcallback, "draw")
    irc.addcommand(uguu.helpcallback, "help")

    while(1):
        irc.parse(bytes.decode(irc.recv()))
        if(not irc.valid):
            irc = twitchchat("drluke4", "oauth:vb6vffy4rqtvon9izfi928g3yoytd1", "#drluke4")
        pri.work()

if(__name__ == "__main__"):
    main()
