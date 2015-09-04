#!/bin/python3

import socket, select, re

class twitchchat:
    def __init__(self, nick, oauth, channel):
        self.server = "irc.twitch.tv"
        self.port = 6667
        self.nick = nick
        self.channel = channel

        self.commands = {} 

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server, self.port))
        
        self.sock.send(str.encode("".join(["PASS ", oauth, "\r\n"])))
        self.sock.send(str.encode("".join(["USER ", nick, " 0 * : DrLuke", "\r\n"])))
        self.sock.send(str.encode("".join(["NICK ", nick, "\r\n"])))
        self.sock.send(str.encode("".join(["JOIN ", channel, "\r\n"])))

    def sendmsg(self, msg):
        self.sock.send(str.encode("".join(["PRIVMSG ", self.channel, " :", msg, "\r\n"])))

    def recvselect(self, timeout):
        return select.select([self.sock],[],[], timeout)
        
    def recv(self):
        out = b""
        contrecv = bool(self.recvselect(0)[0])
        while(contrecv):
            buf = self.sock.recv(4096)
            if(len(buf) < 4096 and not bool(self.recvselect(0)[0])):    #check if there's more to receive 
                contrecv = False
            out += buf
        return out

    def parse(self, inp):
        for line in inp.splitlines():
            match = re.search("".join([":(.+)!(.+) PRIVMSG (", self.channel, ") :(.+)"]), inp)
            if(match):
                print("".join([match.group(1), " in ", match.group(3), " wrote: ", match.group(4)]))
                username = match.group(1)
                channel = match.group(3)
                message = match.group(4)

                self.parsecommand(message, username)
    
    def parsecommand(self, command, username):
        match = re.search("!.+[^\s]", command)
        if(match):
            for name in self.commands:
                commandfun = self.commands[name]
                args = re.findall("(!*\S+)", command)
                if(args[0] == "".join(["!",name])):
                    commandfun([args, username])
                
    def addcommand(self, callback, name):
        self.commands[name] = callback


