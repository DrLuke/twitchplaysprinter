import numpy, subprocess, os

class printer:

    def __init__(self, bot):
        self.currentjob = None
        self.bot = bot

    def work(self):
        if self.currentjob is None:
                self.currentjob = self.bot.getjob()
                if self.currentjob is not None:
                    if(not self.startjob(self.currentjob)):
                        pass # Move Jobfile from new/ to old/
        else:
            if self.subprocess is not None:
                self.subprocess.poll()
                print(bytes.decode(self.subprocess.stdout.read()))
                if self.subprocess.returncode is not None:
                    print(self.subprocess.returncode)
                    if(self.subprocess.returncode == 0):
                        os.rename("new/"+self.currentjob, "old/"+self.currentjob)
                        # Move jobfile from new/ to old/
                    elif(self.subprocess.returncode == 1):
                        os.rename("new/"+self.currentjob, "error/"+self.currentjob)
                        # Move jobfile from new/ to error/
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
     
