from irc import twitchchat
from bot import bot
from printer import printer

def main():
    irc = twitchchat("drluke4", "oauth:vb6vffy4rqtvon9izfi928g3yoytd1", "#drluke4")
    uguu = bot(irc)
    pri = printer(uguu)

    irc.addcommand(uguu.drawmatrixcallback, "draw")
    irc.addcommand(uguu.helpcallback, "help")

    while(1):
        irc.parse(bytes.decode(irc.recv()))
        #pri.work()




if(__name__ == "__main__"):
    main()
