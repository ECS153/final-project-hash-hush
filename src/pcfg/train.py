# 




import sys
from preprocessing import extract_stats

class Preterminal_Stats:
    """Record the Stats for the probabilities of base structs and digits and symbols"""

    def __init__(self):
        """Initialize the dictionaries that store the stats of the training wordlist"""
        # stats of bases
        # data structure: {<base>: <counter>}
        self.bases = {}
        # stats of digit streams, keyed by len 
        # data structure: {<len>: {<digit stream>: <counter>} }
        self.digits = {}
        # stats of symbol streams, keyed by len
        # data structure: {<len>: {<symbol stream: <counter>} }
        self.symbols = {}
        # stats of the dictionary, keyed by len 
        # data structure: {<len>: <count>}
        self.alphas = {}
        # size of the dictionary 
        self.dictSize = 0

    def pw_stats(self, line):
        """generate the relevant stats about the input password"""
        statsOfPw = extract_stats(line)
        if statsOfPw == None:
            return 
        # populate the bases
        base = statsOfPw["base"]
        if base in self.bases:
            self.bases[base] += 1
        else:
            self.bases[base] = 1
        
        # populate the digit streams
        digits = statsOfPw["digits"]
        for digitStream in digits.keys():
            streamLen = len(digitStream)
            counter = digits[digitStream] # number of occurences of that digit stream in that password
            if streamLen in self.digits: # digits table has stats of digit stream of length streamLen
                if digitStream in self.digits[streamLen]:
                    self.digits[streamLen][digitStream] += counter
                else:
                    self.digits[streamLen][digitStream] = counter
            else: 
                self.digits[streamLen] = {}
                self.digits[streamLen][digitStream] = counter
        
        # populate the symbol streams 
        symbols = statsOfPw["symbols"]
        for symbolStream in symbols.keys():
            streamLen = len(symbolStream)
            counter = symbols[symbolStream]
            if streamLen in self.symbols: # digits table has stats of digit stream of length streamLen
                if symbolStream in self.symbols[streamLen]:
                    self.symbols[streamLen][symbolStream] += counter
                else:
                    self.symbols[streamLen][symbolStream] = counter
            else: 
                self.symbols[streamLen] = {}
                self.symbols[streamLen][symbolStream] = counter
    
    def dict_stats(self, line):
        """count the number of words of length n in the dictionary"""

        ## Assume the input dict file is one word per line, delimited by the new line char. The last line of the file is a newline char

        wordLen = len(line) - 1
        if wordLen in self.alphas:
            self.alphas[wordLen] += 1
        else:
            self.alphas[wordLen] = 1

    
    def showBases(self):
        """Show the stats of bases, in decreasing order"""
        allOccurences = sum(self.bases.values())
        sorted_bases = sorted(self.bases.items(), key=lambda x: x[1], reverse=True)
        print ("{:<12} {:<15}".format('Base','Probability'))
        for i in sorted_bases:
            print ("{:<12} {:<15}".format(i[0], i[1]/allOccurences))

    def showDigits(self):
        """Show the stats of digit streams, in decreasing order"""

        for len, digits in self.digits.items():
            print (f"Stats for digit streams of length {len}: ")
            allOccurences = sum(digits.values())
            sorted_digits = sorted(digits.items(), key=lambda x: x[1], reverse=True)
            print ("{:<8} {:<15}".format('Digits','Probability'))
            for i in sorted_digits:
                print ("{:<8} {:<15}".format(i[0], '%.3f'%(i[1]/allOccurences)))
            print()


    def showSymbols(self):
        """Show the stats of symbol streams, in decreasing order"""

        for len, symbols in self.symbols.items():
            print (f"Stats for symbol streams of length {len}: ")
            allOccurences = sum(symbols.values())
            sorted_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)
            print ("{:<8} {:<15}".format('Symbols','Probability'))
            for i in sorted_symbols:
                print ("{:<8} {:<15}".format(i[0], '%.3f'%(i[1]/allOccurences)))
            print()

    def showDict(self):
        """Show the probability of words of length n"""
        print (self.alphas)


def main():
    # requires python 3 or above
    if sys.version_info[0] < 3:
        print("This program requires Python 3.x", file=sys.stderr)
        sys.exit(1)

    # read in the name of the wordlist 
    try:
        wordlist = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <wordlist> <dictionary>")

    # process each line in the input wordlist
    try:
        preterminal_stats = Preterminal_Stats()
        with open(wordlist, encoding='utf-8', errors='ignore') as wordList:
            for line in wordList:
                preterminal_stats.pw_stats(line)
    except FileNotFoundError:
        print (f"Sorry, the file {wordlist} does not exist")

    # read in the name of the dictionary  
    try:
        dictionary = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <wordlist> <dictionary>")

    # process each line in the input dictionary 
    try:
        with open(dictionary, encoding='utf-8', errors='ignore') as dictIonary:
            for line in dictIonary:
                preterminal_stats.dict_stats(line)
    except FileNotFoundError:
        print (f"Sorry, the file {dictionary} does not exist")
    
    #preterminal_stats.showBases()
    #preterminal_stats.showDigits()
   # preterminal_stats.showSymbols()
    preterminal_stats.showDict()
    
if __name__ == "__main__":
    main()