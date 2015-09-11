import numpy, subprocess, os, re

class printer:

    def __init__(self, bot):
        self.currentjob = None
        self.bot = bot

    def work(self):
        if self.currentjob is None:
                self.currentjob = self.bot.getjob()
                if self.currentjob is not None:
                    if(self.startjob(self.currentjob)):
                        pass # Move Jobfile from new/ to error/
                    else:
                        match = re.search("[\d]+_(.*)\.npy",self.currentjob)
                        if(match):
                            self.bot.irc.sendmsg("".join(["@", match.group(1), ": Your image ",self.currentjob, " is being printed next."]))
        else:
            if self.subprocess is not None:
                self.subprocess.poll()
                if self.subprocess.returncode is not None:
                    print(self.subprocess.returncode)
                    if(self.subprocess.returncode == 0):
                        os.rename("new/"+self.currentjob, "old/"+self.currentjob)
                        match = re.search("[\d]+_(.*)\.npy",self.currentjob)
                        if(match):
                            self.bot.irc.sendmsg("".join(["@", match.group(1), ": Your image is done printing!"]))

                    elif(self.subprocess.returncode == 1):
                        os.rename("new/"+self.currentjob, "error/"+self.currentjob)
                        match = re.search("[\d]+_(.*)\.npy",self.currentjob)
                        if(match):
                            self.bot.irc.sendmsg("".join(["@", match.group(1), ": There was an error with your image ",self.currentjob, ". It won't be printed :("]))

                    else:
                        print("Unknown return code: " + str(self.currentjob.returncode))
                    self.currentjob = None

    def startjob(self, newjob):
        self.subprocess = subprocess.Popen(["python", "printjob.py", "new/"+newjob], stdout=subprocess.PIPE)
        self.subprocess.poll()
        if(self.subprocess.returncode is not None):
            self.subprocess = None
            return 1
        return 0
     
