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

    def drawhexcallback(self, args):
        if(len(args) > 2):
            return
        
        match = re.findall("([0-9A-F]+)", args[0][1])
        if(match):
            matrix = self.parsehex(match)
            if(matrix is not None):
                self.adddrawarray(matrix, args[1])
    
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
                rowpixels = re.findall("([0-1])", row)
                rowlist.append(rowpixels)

            # Determine the longest row
            matn = max(len(p) for p in rowlist)
       
            # Pad too short rows with zeros
            for row in rowlist:
                while(len(row) < matn):
                    row.append(0)
            return numpy.flipud(numpy.array(rowlist))
        else:
            return None

    def parsehex(self, args):
        # Check if all values are of same length
        if(all(len(x) == len(args[0]) for x in args)):
            # Clip off all leading all-zero elements
            for x in range(len(args)):
                if args[x] == len(args[x])*'0': # Check if entry is all zeros
                    args[x] = None  # Remove the entry
                else:
                    break   # Stop at first non-zero entry
            
            # Clip off all trailing all-zero elements
            for x in reversed(range(len(args))):
                if args[x] == len(args[x])*'0': # Check if entry is all zeros
                    args[x] = None  # Remove the entry
                else:
                    break   # Stop at first non-zero entry
            
            # Remove all None-elements
            args = list(x for x in args if x is not None)

            # Convert hexadecimal to binary for easier processing
            for x in range(len(args)):
                args[x] = bin(int(args[x], 16))[2:].zfill(len(args[x])*4)
            
            # Split string into list of pixel values
            rows = list(args)
            for x in range(len(args)):
                rows[x] = re.findall("[01]",args[x])
           
            # Find all-zero columns on left edge of matrix
            for pos in range(len(rows[0])):
                print(rows)
                if(all([x[pos] == '0' for x in rows])):
                    for x in rows:
                        x[pos] = None
                else:
                    break
            
            # Find all-zero columns on right edge of matrix
            for pos in reversed(range(len(rows[0]))):
                if(all([x[pos] == '0' for x in rows])):
                    for x in rows:
                        x[pos] = None
                else:
                    break
           
            # Remove all None-Elements
            for pos in range(len(rows)):
                rows[pos] = [x for x in rows[pos] if x is not None]
            

            # Create numpy matrix from list
            return numpy.flipud(numpy.array(rows))
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
        helpdict["draw"] = "Draw an image supplied in form of a matrix. Each bracket contains a single row with 0 and 1 as pixel values. Syntax: \"!draw <matrix>\" Example: !draw [[10101],[11101],[10101]] will print 'HI'. You can use any dimensions you like, the image will be autoscaled."
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

        try:
            returnfile = retfile[0]
            return returnfile
        except:
            return None        
