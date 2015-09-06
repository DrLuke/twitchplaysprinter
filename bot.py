import re,numpy,os

class bot:
    sequentialfileid = 0

    def __init__(self,irc):
        self.irc = irc 
        self.determinehighestseqnum()

    def drawmatrixcallback(self, args):

        drawarray = self.parsematrix(" ".join(args[0]))
        if(isinstance(drawarray, numpy.ndarray)):
            self.adddrawarray(drawarray, args[1])
        else:
            self.irc.sendmsg("".join(["@", args[1], ": Invalid matrix format. See !help draw"]))
    
    def adddrawarray(self, array, username):
        """ Saves an array which shall be drawn later """
        numpy.save("".join(["new/", str(bot.sequentialfileid), "_", username]), array)
        bot.sequentialfileid += 1

    def parsematrix(self, matrix):
        """ Tries to find and parse a matrix in a string """
        rowlist = []

        # Find the matrix in the input string
        match = re.search("(?<!\[)\[((?:\[(?:\d+,)*\d+\],)*(?:\[(?:\d+,)*\d+\]))\](?!\])", matrix)
        if(match):
            # Find all the individual rows of matrix
            rows = re.findall("(\[[0-9,]*\])",match.group(1))
            for row in rows:
                rowpixels = re.findall("([1-9]+(?=\,|\]))", row)
                rowlist.append(rowpixels)

            # Determine the longest row
            matn = max(len(p) for p in rowlist)
       
            # Pad too short rows with zeros
            for row in rowlist:
                while(len(row) < matn):
                    row.append(0)
            return numpy.array(rowlist)
        else:
            return None

    def determinehighestseqnum(self):
        try:
            filenames = []
            for (dirp, dirn, fn) in os.walk("new"):
                filenames += fn
                break

            for (dirp, dirn, fn) in os.walk("old"):
                filenames += fn
                break

            nums = []
            for filename in filenames:
                nums.append(int(re.findall("([\d]*)_",filename)[0]))
            bot.sequentialfileid = max(nums)+1
        except:
            bot.sequentialfileid = 0

    def helpcallback(self, args):
        helpdict = {}
        helpdict["default"] = "Write \"!command <arguments>\" to send commands to the printer. For a list of available commands, write \"!help commands\". For help with each commands, type \"!help <commandname>\"."
        helpdict["commands"] = "draw - help"
        helpdict["draw"] = "Draw an image supplied in form of a matrix. Each bracket contains a single row with 0 and 1 as pixel values. Syntax: \"!draw <matrix>\" Example: !draw [[1,0,1,0,1],[1,1,1,0,1],[1,0,1,0,1]]. You can use any dimensions you like, the image will be autoscaled."
        helpdict["help"] = "No eastereggs here"
        helpdict["easteregg"] = "I lied"
        helpdict["dickbutt"] = "Dickbutts galore!"
        

        try:
            self.irc.sendmsg("".join(["@", args[1], ": ", helpdict[args[0][1]]]))
        except:
            self.irc.sendmsg("".join(["@", args[1], ": ", helpdict["default"]]))

    def getjob(self):
        retfile = []
        for (dirp, dirn, fn) in os.walk("new"):
            retfile = fn
            break

        if(retfile[0]):
            return retfile[0]
        else:
            return None

